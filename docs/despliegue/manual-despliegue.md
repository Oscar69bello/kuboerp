# KuboERP · Manual de despliegue

La misma imagen Docker de KuboERP se ejecuta en tres ambientes. Todos leen la cadena de conexión de la variable
`ConnectionStrings__KuboERP` y exponen la sonda de salud `/health`.

| Ambiente | Herramienta | Base de datos | URL |
|---|---|---|---|
| Local | Docker Compose | SQL Server 2022 en contenedor | http://localhost:8080 |
| Clúster | Kubernetes (Docker Desktop o kind) | SQL Server 2022 en StatefulSet | http://localhost:8081 |
| Nube | Azure Container Apps | Azure SQL Database (oferta gratuita) | Ver `deploy/azure/.secretos.local` o el documento final |

## Requisitos
- Windows 10/11 con virtualización activa, **WSL 2** y **Docker Desktop** (`winget install Docker.DockerDesktop`).
- **Azure CLI** (`winget install Microsoft.AzureCLI`) y una suscripción (Azure for Students: USD 100 sin tarjeta).
- Para Kubernetes local: activar *Settings → Kubernetes → Enable Kubernetes* en Docker Desktop.

## 1. Docker Compose
```powershell
cd dotnet
Copy-Item .env.example .env        # y cambiar SQL_SA_PASSWORD por una clave segura
docker compose up -d --build
docker compose ps                  # ambos servicios en estado "healthy"
curl http://localhost:8080/health  # Healthy
```
Detener: `docker compose down` (agregar `-v` para borrar también los datos).

## 2. Kubernetes
```powershell
docker build -t kuboerp-web:local dotnet
kubectl apply -f k8s/00-namespace.yaml
$clave = "Kb" + [Guid]::NewGuid().ToString("N").Substring(0,16) + "#1"
kubectl -n kuboerp create secret generic kuboerp-sql `
  --from-literal=sa-password=$clave `
  --from-literal=connection-string="Server=sql,1433;Database=KuboERP;User Id=sa;Password=$clave;TrustServerCertificate=True;MultipleActiveResultSets=true"
kubectl apply -k k8s/
kubectl -n kuboerp rollout status deployment/web
kubectl -n kuboerp get pods,svc,hpa
```
La aplicación queda en http://localhost:8081. Eliminar todo: `kubectl delete namespace kuboerp`.

Recursos del clúster:

| Recurso | Nombre | Propósito |
|---|---|---|
| Namespace | `kuboerp` | Aísla los recursos del ERP |
| Secret | `kuboerp-sql` | Contraseña de SQL Server y cadena de conexión (no se versiona) |
| StatefulSet + Service headless | `sql` | SQL Server con volumen persistente de 5 Gi |
| Deployment | `web` | 2 réplicas, actualización sin caída, sondas startup/liveness/readiness |
| Service LoadBalancer | `web` | Publica la aplicación en el puerto 8081 |
| HorizontalPodAutoscaler | `web` | Escala de 2 a 5 réplicas al 70 % de CPU |

## 3. Microsoft Azure
```powershell
az login
.\deploy\azure\desplegar.ps1                  # primer despliegue (10–15 min)
.\deploy\azure\desplegar.ps1 -Version v1.1    # nueva versión
```
El script crea en el grupo `rg-kuboerp-prod`:

| Recurso | Configuración |
|---|---|
| Azure Container Registry (Basic) | Construye la imagen en la nube con `az acr build`; no requiere Docker local |
| Azure SQL Database | Serverless con oferta gratuita y pausa automática; TLS 1.2; firewall solo para servicios de Azure |
| Container Apps Environment + Container App | HTTPS público, 0,5 vCPU y 1 GiB, 1 a 3 réplicas; descarga la imagen con identidad administrada |

Ver el estado y los registros:
```powershell
az containerapp show -n kuboerp-web -g rg-kuboerp-prod --query properties.configuration.ingress.fqdn -o tsv
az containerapp logs show -n kuboerp-web -g rg-kuboerp-prod --tail 50
```
Eliminar todo al terminar el semestre (detiene el consumo de crédito): `az group delete -n rg-kuboerp-prod`.

## Seguridad
- Ninguna contraseña está en el repositorio: `.env`, los Secrets de Kubernetes y los secretos de Container Apps se
  crean al desplegar. La clave de Azure SQL se genera al azar y queda solo en `deploy/azure/.secretos.local` (ignorado por Git).
- La imagen corre con un usuario sin privilegios; en Kubernetes se quitan todas las capacidades de Linux.
- El TLS termina en el balanceador; la aplicación confía en `X-Forwarded-Proto` para generar enlaces https.
