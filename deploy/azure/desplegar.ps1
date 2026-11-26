<#
.SYNOPSIS
  KuboERP · Despliegue en Microsoft Azure (Azure for Students).

.DESCRIPTION
  Crea, en un grupo de recursos propio:
    1. Azure Container Registry (Basic); la imagen se construye con Docker local y se sube con docker push
       (Azure for Students no permite ACR Tasks / az acr build). Requiere Docker Desktop encendido.
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
    # Azure for Students solo permite algunas regiones (política "Allowed resource deployment regions"):
    # northcentralus, brazilsouth, spaincentral, chilecentral, canadacentral. Brazil South es la más cercana a Colombia.
    [string]$Region = "brazilsouth",
    [string]$GrupoRecursos = "rg-kuboerp-prod",
    [string]$Version = "v1.0"
)
# Sin ErrorActionPreference=Stop: en PowerShell 5.1 convierte los avisos de az en errores. Az() valida cada paso.
$raiz = Resolve-Path "$PSScriptRoot\..\.."
$archivoSecretos = Join-Path $PSScriptRoot ".secretos.local"

function Paso($texto) { Write-Host "`n==> $texto" -ForegroundColor Cyan }
$script:claveSql = $null
$script:ocultos = @()
# Ejecuta az y detiene el script si falla; las claves (SQL y registro) nunca se muestran en el mensaje de error
function Invoke-Az {
    & az.cmd @args
    if ($LASTEXITCODE -ne 0) {
        $comando = "az " + ($args -join ' ')
        foreach ($s in @($script:claveSql) + $script:ocultos) { if ($s) { $comando = $comando.Replace($s, "****") } }
        throw "Falló: $comando"
    }
}

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
    if ((az provider show --namespace $ns --query registrationState -o tsv) -ne "Registered") {
        Invoke-Az provider register --namespace $ns --wait | Out-Null
    }
}
# Solo se instala la extensión si falta: buscar actualizaciones (--upgrade) a veces se queda colgado en "Searching"
if (-not (az extension show --name containerapp --query name -o tsv 2>$null)) {
    Invoke-Az extension add --name containerapp --only-show-errors | Out-Null
}

Paso "Grupo de recursos $GrupoRecursos en $Region"
if ((az group exists -n $GrupoRecursos) -ne "true") {
    Invoke-Az group create -n $GrupoRecursos -l $Region --tags proyecto=KuboERP sprint=4 -o none
}

Paso "Azure Container Registry $acr"
if (-not (az acr show -n $acr -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az acr create -n $acr -g $GrupoRecursos -l $Region --sku Basic -o none
}

# Azure for Students no permite ACR Tasks (az acr build): la imagen se construye con Docker local y se sube al registro
Paso "Construcción local de la imagen $imagen y envío al registro"
function Invoke-Docker { & docker @args; if ($LASTEXITCODE -ne 0) { throw "Falló: docker $($args -join ' ')" } }
# Reintenta pasos de red (login y push): un corte momentáneo de la conexión no debe tumbar el despliegue
function Invoke-Reintentos([scriptblock]$accion, [string]$nombre) {
    for ($i = 1; $i -le 3; $i++) {
        try { & $accion; return }
        catch {
            if ($i -eq 3) { throw }
            Write-Host "  $nombre falló (intento $i de 3); se reintenta en 10 segundos..." -ForegroundColor Yellow
            Start-Sleep -Seconds 10
        }
    }
}
Invoke-Docker build -t $imagen -t "$acr.azurecr.io/kuboerp-web:latest" "$raiz\dotnet"
Invoke-Reintentos { Invoke-Az acr login -n $acr } "El inicio de sesión en el registro"
Invoke-Reintentos { Invoke-Docker push $imagen } "El envío de la imagen"
Invoke-Reintentos { Invoke-Docker push "$acr.azurecr.io/kuboerp-web:latest" } "El envío de la etiqueta latest"

Paso "Azure SQL: servidor y base de datos $baseDatos (oferta gratuita)"
if (Test-Path $archivoSecretos) {
    $script:claveSql = (Get-Content $archivoSecretos | Where-Object { $_ -like "SQL_PASSWORD=*" }) -replace "^SQL_PASSWORD=", ""
} else {
    $script:claveSql = "Kb" + [Guid]::NewGuid().ToString("N").Substring(0, 20) + "#9"
    "SQL_PASSWORD=$script:claveSql" | Out-File $archivoSecretos -Encoding utf8
}
$claveSql = $script:claveSql

# Algunas regiones dejan de aceptar servidores nuevos de Azure SQL por capacidad (RegionDoesNotAllowProvisioning):
# se prueba primero $Region y luego las demás regiones que permite Azure for Students.
# Un intento fallido deja el nombre reservado en esa región, así que cada región usa un nombre propio.
$existente = az sql server list -g $GrupoRecursos --query "[0].[name, location]" -o tsv 2>$null
if ($existente) { $servidorSql, $regionDatos = $existente -split "\s+" } else { $regionDatos = $null }
if (-not $regionDatos) {
    $candidatas = @($Region, "brazilsouth", "canadacentral", "northcentralus", "spaincentral", "chilecentral") | Select-Object -Unique
    foreach ($r in $candidatas) {
        $nombre = "sql-kuboerp-$sufijo-$r"
        Write-Host "  Creando el servidor de Azure SQL $nombre en $r..."
        $salida = az sql server create -n $nombre -g $GrupoRecursos -l $r -u kuboadmin -p $claveSql --minimal-tls-version 1.2 -o none 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) { $servidorSql = $nombre; $regionDatos = $r; break }
        $motivo = ($salida -split "`n" | Where-Object { $_ -like "*Code:*" } | Select-Object -First 1)
        Write-Host "  $r no aceptó el servidor ($($motivo.Trim())); se prueba la siguiente región." -ForegroundColor Yellow
    }
    if (-not $regionDatos) { throw "Ninguna región permitida aceptó el servidor de Azure SQL. Intente más tarde." }
    # 0.0.0.0 = permite solo el tráfico que sale de servicios de Azure (Container Apps); no abre la base a Internet
    Invoke-Az sql server firewall-rule create -g $GrupoRecursos -s $servidorSql -n AllowAzureServices --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 -o none
}
Write-Host "  Servidor de Azure SQL en $regionDatos"
if (-not (az sql db show -n $baseDatos -s $servidorSql -g $GrupoRecursos --query name -o tsv 2>$null)) {
    az sql db create -g $GrupoRecursos -s $servidorSql -n $baseDatos --edition GeneralPurpose --family Gen5 --capacity 2 `
        --compute-model Serverless --use-free-limit --free-limit-exhaustion-behavior AutoPause -o none
    if ($LASTEXITCODE -ne 0) {
        Write-Host "La oferta gratuita no está disponible; se usa el nivel Basic (unos USD 5 al mes del crédito)." -ForegroundColor Yellow
        Invoke-Az sql db create -g $GrupoRecursos -s $servidorSql -n $baseDatos --service-objective Basic -o none
    }
}
$cadena = "Server=tcp:$servidorSql.database.windows.net,1433;Database=$baseDatos;User ID=kuboadmin;Password=$claveSql;Encrypt=True;TrustServerCertificate=False;MultipleActiveResultSets=True;Connection Timeout=60"

# La aplicación va en la misma región que la base de datos para que las consultas no crucen continentes
Paso "Ambiente de Azure Container Apps $ambiente en $regionDatos"
if (-not (az containerapp env show -n $ambiente -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Az containerapp env create -n $ambiente -g $GrupoRecursos -l $regionDatos -o none
}

# Los ambientes "express" de Container Apps no permiten descargar la imagen con identidad administrada:
# se usa el usuario administrador del registro, guardado como secreto de la Container App.
Paso "Credenciales del registro $acr para Container Apps"
Invoke-Az acr update -n $acr --admin-enabled true -o none
$usuarioAcr = az acr credential show -n $acr --query username -o tsv
$claveAcr = az acr credential show -n $acr --query "passwords[0].value" -o tsv
if (-not $claveAcr) { throw "No se pudieron leer las credenciales del registro $acr" }
$script:ocultos += $claveAcr

Paso "Container App $app con la imagen $imagen"
# Una versión anterior del script creaba la app con identidad administrada; en ambientes express esa app
# ya no se puede modificar (ni quitarle la identidad), así que se borra y se crea de nuevo. La base de datos no se toca.
$identidad = az resource show -g $GrupoRecursos -n $app --resource-type Microsoft.App/containerApps --query identity.type -o tsv 2>$null
if ($identidad -like "*SystemAssigned*") {
    Write-Host "  La app $app quedó con identidad administrada (no admitida en ambientes express); se borra y se crea de nuevo." -ForegroundColor Yellow
    Invoke-Az resource delete -g $GrupoRecursos -n $app --resource-type Microsoft.App/containerApps
}
if (-not (az containerapp show -n $app -g $GrupoRecursos --query name -o tsv 2>$null)) {
    Invoke-Reintentos {
        Invoke-Az containerapp create -n $app -g $GrupoRecursos --environment $ambiente `
            --image $imagen --registry-server "$acr.azurecr.io" --registry-username $usuarioAcr --registry-password $claveAcr `
            --target-port 8080 --ingress external --cpu 0.5 --memory 1.0Gi --min-replicas 1 --max-replicas 3 `
            --secrets "sql-conn=$cadena" `
            --env-vars "ConnectionStrings__KuboERP=secretref:sql-conn" "ASPNETCORE_ENVIRONMENT=Production" -o none
    } "La creación de la Container App"
} else {
    Invoke-Az containerapp registry set -n $app -g $GrupoRecursos --server "$acr.azurecr.io" --username $usuarioAcr --password $claveAcr -o none
    Invoke-Az containerapp secret set -n $app -g $GrupoRecursos --secrets "sql-conn=$cadena" -o none
    Invoke-Az containerapp ingress enable -n $app -g $GrupoRecursos --type external --target-port 8080 -o none
    Invoke-Az containerapp update -n $app -g $GrupoRecursos --image $imagen `
        --cpu 0.5 --memory 1.0Gi --min-replicas 1 --max-replicas 3 `
        --set-env-vars "ConnectionStrings__KuboERP=secretref:sql-conn" "ASPNETCORE_ENVIRONMENT=Production" -o none
}

$url = "https://" + (az containerapp show -n $app -g $GrupoRecursos --query properties.configuration.ingress.fqdn -o tsv)
"URL=$url" | Out-File $archivoSecretos -Append -Encoding utf8
Paso "Listo. KuboERP quedó publicado en: $url"
Write-Host "Salud de la aplicación: $url/health (el primer arranque tarda 1 o 2 minutos mientras crea la base)."
