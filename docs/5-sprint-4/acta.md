# Sprint 4 · Despliegue: Docker, Kubernetes y nube

**De Visual Studio a producción** · 24 de noviembre al 4 de diciembre de 2026 · Sprint final
Responsable: Oscar Javier Bello Daza

## Sprint Planning
**Objetivo del sprint:** publicar KuboERP en Internet de forma reproducible: la misma imagen Docker corre en el
equipo del desarrollador, en un clúster de Kubernetes y en Microsoft Azure, verificada automáticamente en cada push.

| ID | Historia técnica | Criterio de aceptación |
|---|---|---|
| HT-04 | Contenerizar la aplicación | `docker compose up` levanta web + SQL Server y `/health` responde *Healthy* |
| HT-05 | Orquestar con Kubernetes | `kubectl apply -k k8s/` despliega 2 réplicas con sondas y escalado automático |
| HT-06 | Desplegar en Azure | URL pública con HTTPS en Azure Container Apps y base de datos en Azure SQL |
| HT-07 | Pipeline de entrega | GitHub Actions compila, prueba la imagen con Compose y despliega en un clúster kind |
| HT-08 | Cierre del proyecto | Documentación final, sustentación y acta de cierre |

## Trabajo realizado
| Artefacto | Ubicación | Descripción |
|---|---|---|
| Sondas de salud y configuración por entorno | `dotnet/KuboERP.Web/Program.cs` | `/health/vivo` (liveness), `/health` (readiness con SQL), reintentos y cabeceras del proxy |
| Imagen Docker | `dotnet/Dockerfile` | Compilación en dos etapas, runtime ASP.NET 10, usuario sin privilegios, puerto 8080 |
| Ambiente local | `dotnet/docker-compose.yml` | Web + SQL Server 2022 con volumen persistente y healthcheck |
| Kubernetes | `k8s/` | Namespace, StatefulSet de SQL Server, Deployment de 2 réplicas, Service y HPA |
| Despliegue en Azure | `deploy/azure/desplegar.ps1` | Container Registry, Azure SQL (oferta gratuita) y Container Apps |
| Integración continua | `.github/workflows/ci.yml` | Jobs `dotnet`, `docker` y `kubernetes` además de Python y Terraform |

## Sprint Review
Ver el documento final de entrega (`docs/6-cierre/`) para la demostración, el enlace de despliegue y la evidencia.

## Retrospectiva
| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Construir la imagen en Azure (`az acr build`) evitó depender de Docker local para desplegar | Docker Desktop exige WSL 2 y reinicio | Documentar los requisitos en el manual de despliegue |
| La sonda de salud separa "proceso vivo" de "base disponible" | SQL Server tarda en arrancar en contenedores | Reintentos al inicio y `startupProbe` en Kubernetes |
| El pipeline prueba Compose y Kubernetes en cada push | La cadena de conexión usa usuario y contraseña de SQL | Migrar a identidad administrada de Entra ID |
