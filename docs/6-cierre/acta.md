# Cierre del proyecto · KuboERP

**ERP de ElectroSoluciones S.A.S. publicado en Internet** · Fecha de cierre: 25 de noviembre de 2026
Responsable: Oscar Javier Bello Daza (Product Owner, Scrum Master y equipo de desarrollo)

## Aplicación en producción

| Ambiente | Cómo se ejecuta | Base de datos | Dirección |
|---|---|---|---|
| **Nube (producción)** | Azure Container Apps, Spain Central, 1 a 3 réplicas | Azure SQL Database (nivel Basic) | **https://kuboerp-web.agreeableglacier-e55852c8.spaincentral.azurecontainerapps.io** |
| Clúster | Kubernetes de Docker Desktop (kubeadm v1.36.1), 2 réplicas + HPA | SQL Server 2022 en StatefulSet | http://localhost:8081 |
| Local | Docker Compose | SQL Server 2022 en contenedor | http://localhost:8080 |
| Desarrollo | Visual Studio 2026 / `dotnet run` | SQL Server LocalDB | http://localhost:5174 |

Los tres primeros ambientes ejecutan **la misma imagen Docker** (`dotnet/Dockerfile`). La sonda `/health` responde
*Healthy* cuando la aplicación tiene conexión con la base de datos. Pasos completos en el
[manual de despliegue](../despliegue/manual-despliegue.md).

## Resumen de las iteraciones

| Iteración | Fecha | Resultado | Acta |
|---|---|---|---|
| Inicio | 6 sep | Acta de constitución, 4 épicas y 16 historias (97 SP) con Planning Poker | [0-inicio](../0-inicio/acta.md) |
| Sprint 0 | 13 sep | Problema y solución, modelo 4+1, arquitectura en capas + DDD, stack Microsoft | [1-sprint-0](../1-sprint-0/acta.md) |
| Sprint 1 | 12 oct | 7 épicas, 41 historias (212 SP), Definition of Done, diagramas, mockups en Figma | [2-sprint-1](../2-sprint-1/acta.md) |
| Sprint 2 | 2 y 14 nov | Dominio con TDD/BDD (cobertura 100 %), Terraform, GitHub Actions, arc42 | [3-sprint-2](../3-sprint-2/acta.md) |
| Sprint 3 | 21 nov | ERP en ASP.NET Core MVC + SQL Server: 7 módulos y tablero gerencial | [4-sprint-3](../4-sprint-3/acta.md) |
| Sprint 4 | 25 nov | Docker, Kubernetes, Azure Container Apps y pipeline de entrega | [5-sprint-4](../5-sprint-4/acta.md) |

## Sprint Review del Sprint 4

| ID | Historia técnica | Criterio de aceptación | Resultado | Evidencia |
|---|---|---|---|---|
| HT-04 | Contenerizar la aplicación | `docker compose up` levanta web + SQL Server y `/health` responde *Healthy* | ✔ Ambos contenedores *healthy*; tablero en el puerto 8080 | [01](evidencias/01_docker_compose_contenedores.png), [02](evidencias/02_tablero_docker_8080.png) |
| HT-05 | Orquestar con Kubernetes | `kubectl apply -k k8s/` despliega 2 réplicas con sondas y escalado automático | ✔ Deployment `web` 2/2, `sql-0` Running, Service en el puerto 8081 | [03](evidencias/03_kubernetes_docker_desktop.png) |
| HT-06 | Desplegar en Azure | URL pública con HTTPS en Azure Container Apps y base de datos en Azure SQL | ✔ `/health` *Healthy*; http redirige a https | URL de producción |
| HT-07 | Pipeline de entrega | GitHub Actions compila, prueba la imagen con Compose y despliega en kind | Ver la pestaña *Actions* de la rama `sprint-4/despliegue-docker-kubernetes` | GitHub Actions |
| HT-08 | Cierre del proyecto | Documentación final y acta de cierre | ✔ Este documento | — |

**Definition of Done**

| Criterio | Estado |
|---|---|
| Código versionado en GitHub | ✔ |
| Pruebas automáticas en verde (escenarios BDD con Reqnroll) | ✔ 3 de 3 |
| Despliegue reproducible desde el repositorio | ✔ Docker Compose, manifiestos de Kubernetes y `deploy/azure/desplegar.ps1` |
| Ninguna contraseña en el repositorio | ✔ `.env`, Secret de Kubernetes y secretos de Container Apps se crean al desplegar |
| Revisión por pull request de un compañero | ✘ El trabajo fue individual |

## Recursos en Azure (grupo `rg-kuboerp-prod`)

| Recurso | Región | Nota |
|---|---|---|
| Azure Container Registry (Basic) `acrkuboerpbcc907` | Brazil South | Imagen `kuboerp-web:v1.0` |
| Azure SQL: servidor `sql-kuboerp-bcc907-spaincentral`, base `KuboERP` (Basic) | Spain Central | La oferta gratuita no estaba disponible en la región |
| Container Apps: ambiente `cae-kuboerp` y app `kuboerp-web` | Spain Central | HTTPS público, 0,5 vCPU y 1 GiB |

Al terminar el semestre se elimina todo con `az group delete -n rg-kuboerp-prod` para no consumir más crédito.

## Retrospectiva final

| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Una sola imagen Docker sirvió para los tres ambientes sin cambios de código | Azure for Students restringe regiones, no permite ACR Tasks y la región elegida no aceptaba Azure SQL | El script prueba las regiones permitidas, construye con Docker local y reintenta los pasos de red |
| Las sondas de salud separan "proceso vivo" de "base disponible" y Kubernetes solo envía tráfico a réplicas listas | Los ambientes *express* de Container Apps no admiten identidad administrada para el registro | Usar las credenciales del registro guardadas como secreto |
| Las reglas de negocio probadas en Python en el Sprint 2 se mantuvieron hasta producción | La consola de PowerShell se pausa al hacer clic (modo de edición rápida) | Desactivar la edición rápida durante despliegues largos |
| El pipeline prueba Compose y Kubernetes en cada push | La cadena de conexión usa usuario y contraseña de SQL | Migrar a identidad administrada de Entra ID en un ambiente con perfiles de carga |

## Trabajo futuro (Product Backlog pendiente)
Las épicas de comercio electrónico (EP01 catálogo y compra en línea), servicios técnicos (EP02), clientes (EP03) y
garantías (EP04) siguen en el Product Backlog. También quedan pendientes la autenticación de usuarios con Entra ID,
una API documentada con Swagger y el monitoreo con Application Insights.
