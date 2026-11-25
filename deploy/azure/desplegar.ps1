<#
.SYNOPSIS
  KuboERP · Despliegue en Microsoft Azure (Azure for Students).

.DESCRIPTION
  Crea, en un grupo de recursos propio:
    1. Azure Container Registry (Basic) y construye la imagen Docker en la nube (az acr build).
    2. Azure SQL Database con la oferta gratuita (serverless, se pausa sola).
    3. Azure Container Apps (Kubernetes administrado con KEDA) que ejecuta la imagen con HTTPS público.
  La contraseña de SQL se genera al azar, se guarda como secreto de Container Apps y en un archivo local
  fuera de Git (deploy/azure/.secretos.local). Nunca se escribe en el repositorio.

.EXAMPLE
  az login
  .\deploy\azure\desplegar.ps1                       # primer despliegue
  .\deploy\azure\desplegar.ps1 -Version v1.1         # nueva versión: reconstruye la imagen y actualiza la app
#>
param(
    [string]$Region = "eastus2",
    [string]$GrupoRecursos = "rg-kuboerp-prod",
    [string]$Version = "v1.0"
)
# Sin ErrorActionPreference=Stop: en PowerShell 5.1 convierte los avisos de az en errores. Az() valida cada paso.
$raiz = Resolve-Path "$PSScriptRoot\..\.."
$archivoSecretos = Join-Path $PSScriptRoot ".secretos.local"

function Paso($texto) { Write-Host "`n==> $texto" -ForegroundColor Cyan }
function Invoke-Az { & az.cmd @args; if ($LASTEXITCODE -ne 0) { throw "Falló: az $($args -join ' ')" } }

# Sufijo estable por suscripción para que los nombres globales (ACR, SQL) sean únicos
$suscripcion = (az account show --query id -o tsv)
if (-not $suscripcion) { throw "Primero inicie sesión con: az login" }
$sufijo = $suscripcion.Substring(0, 6).ToLower()
$acr = "acrkuboerp$sufijo"
$servidorSql = "sql-kuboerp-$sufijo"
$baseDatos = "KuboERP"
$ambiente = "cae-kuboerp"
$app = "kuboerp-web"
$imagen = "$acr.azurecr.io/kuboerp-web:$Version"

Paso "Registrando los proveedores de recursos (solo tarda la primera vez)"
foreach ($ns in "Microsoft.App", "Microsoft.OperationalInsights", "Microsoft.ContainerRegistry", "Microsoft.Sql") {
    Invoke-Az provider register --namespace $ns --wait | Out-Null
}
Invoke-Az extension add --name containerapp --upgrade --only-show-errors | Out-Null

Paso "Grupo de recursos $GrupoRecursos en $Region"
Invoke-Az group create -n $GrupoRecursos -l $Region --tags proyecto=KuboERP sprint=4 -o none

Paso "Azure Container Registry $acr y construcción de la imagen $imagen en la nube"
if (-not (az acr show -n $acr -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az acr create -n $acr -g $GrupoRecursos --sku Basic -o none
}
Invoke-Az acr build -r $acr -t "kuboerp-web:$Version" -t "kuboerp-web:latest" "$raiz\dotnet"

Paso "Azure SQL $servidorSql / $baseDatos (oferta gratuita)"
if (Test-Path $archivoSecretos) {
    $claveSql = (Get-Content $archivoSecretos | Where-Object { $_ -like "SQL_PASSWORD=*" }) -replace "^SQL_PASSWORD=", ""
} else {
    $claveSql = "Kb" + [Guid]::NewGuid().ToString("N").Substring(0, 20) + "#9"
    "SQL_PASSWORD=$claveSql" | Out-File $archivoSecretos -Encoding utf8
}
if (-not (az sql server show -n $servidorSql -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az sql server create -n $servidorSql -g $GrupoRecursos -l $Region -u kuboadmin -p $claveSql --minimal-tls-version 1.2 -o none
    # 0.0.0.0 = permite solo el tráfico que sale de servicios de Azure (Container Apps); no abre la base a Internet
    Invoke-Az sql server firewall-rule create -g $GrupoRecursos -s $servidorSql -n AllowAzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 -o none
}
if (-not (az sql db show -n $baseDatos -s $servidorSql -g $GrupoRecursos --query name -o tsv 2>$null)) {
    az sql db create -g $GrupoRecursos -s $servidorSql -n $baseDatos --edition GeneralPurpose --family Gen5 --capacity 2 `
        --compute-model Serverless --use-free-limit --free-limit-exhaustion-behavior AutoPause -o none
    if ($LASTEXITCODE -ne 0) {
        Write-Host "La oferta gratuita no está disponible; se usa el nivel Basic (unos USD 5 al mes del crédito)." -ForegroundColor Yellow
        Invoke-Az sql db create -g $GrupoRecursos -s $servidorSql -n $baseDatos --service-objective Basic -o none
    }
}
$cadena = "Server=tcp:$servidorSql.database.windows.net,1433;Database=$baseDatos;User ID=kuboadmin;Password=$claveSql;Encrypt=True;TrustServerCertificate=False;MultipleActiveResultSets=True;Connection Timeout=60"

Paso "Ambiente de Azure Container Apps $ambiente"
if (-not (az containerapp env show -n $ambiente -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az containerapp env create -n $ambiente -g $GrupoRecursos -l $Region -o none
}

Paso "Container App $app con la imagen $imagen"
if (-not (az containerapp show -n $app -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az containerapp create -n $app -g $GrupoRecursos --environment $ambiente `
        --image $imagen --registry-server "$acr.azurecr.io" --registry-identity system `
        --target-port 8080 --ingress external --cpu 0.5 --memory 1.0Gi --min-replicas 1 --max-replicas 3 `
        --secrets "sql-conn=$cadena" `
        --env-vars "ConnectionStrings__KuboERP=secretref:sql-conn" "ASPNETCORE_ENVIRONMENT=Production" -o none
} else {
    Invoke-Az containerapp secret set -n $app -g $GrupoRecursos --secrets "sql-conn=$cadena" -o none
    Invoke-Az containerapp update -n $app -g $GrupoRecursos --image $imagen -o none
}

$url = "https://" + (az containerapp show -n $app -g $GrupoRecursos --query properties.configuration.ingress.fqdn -o tsv)
"URL=$url" | Out-File $archivoSecretos -Append -Encoding utf8
Paso "Listo. KuboERP quedó publicado en: $url"
Write-Host "Salud de la aplicación: $url/health (el primer arranque tarda 1 o 2 minutos mientras crea la base)."
