# KuboERP · Gestión ágil del proyecto

Documentación de las iteraciones del proyecto **KuboERP**, el ERP de **ElectroSoluciones S.A.S.**, empresa que
comercializa materiales eléctricos y presta servicios técnicos de instalación, mantenimiento y reparación.
Hasta el Sprint 0 el proyecto se llamó *ElectroSoluciones Digital*; desde el Sprint 1 se llama **KuboERP**.

| | |
|---|---|
| **Estudiante** | Oscar Javier Bello Daza |
| **Programa** | Ingeniería de Sistemas y Computación · Semestre 6 · Grupo 601N SIS |
| **Materia** | Proyecto de Ingeniería de Software II |
| **Profesor** | Carlos Eduardo Mujica Reyes |
| **Institución** | Universidad de Cundinamarca · Extensión Chía |

## Marco de trabajo y roles

Se trabaja con **Scrum**. Oscar Javier Bello Daza asume los tres roles del equipo de trabajo:

| Rol | Responsabilidad |
|---|---|
| **Product Owner** | Define y prioriza el Product Backlog (MoSCoW) y acepta cada incremento contra sus criterios de aceptación. |
| **Scrum Master** | Organiza las ceremonias, cuida el cronograma y registra impedimentos y mejoras. |
| **Equipo de desarrollo** | Diseña, implementa y prueba el incremento de cada sprint. |

El seguimiento del trabajo se lleva en el tablero **GitHub Projects · KuboERP · Scrum**, ligado a este
repositorio: cada iteración es un *milestone* y cada historia o tarea es un *issue*.

En el producto simulado, el Product Owner representa a la Gerencia Comercial de ElectroSoluciones S.A.S. y el
patrocinador es su Gerencia General (Acta de Constitución).

## Cronograma de iteraciones

| Iteración | Entrega | Tema | Resultado | Acta |
|---|---|---|---|---|
| Inicio | 6 sep 2026 | "Difícil de ver, el futuro es" · Concepto, planeación y estimación ágil | Acta de constitución, 4 épicas, 16 historias, backlog estimado con Planning Poker (97 SP), matriz de interesados | [0-inicio](0-inicio/acta.md) |
| Sprint 0 | 13 sep 2026 | "Prepara tu nave" · Definición del proyecto y plataformas | Problema y solución, modelo 4+1, arquitectura en capas + DDD, árbol de 6 módulos, requisitos no funcionales, stack Microsoft, presupuesto | [1-sprint-0](1-sprint-0/acta.md) |
| Sprint 1 | 12 oct 2026 | Diseño y especificación del ERP + Video Figma | KuboERP: Event Storming, 36 RF, 17 RNF, 7 épicas y 41 historias (212 SP), Definition of Done, diagramas PlantUML, mockups y video de los CRUD | [2-sprint-1](2-sprint-1/acta.md) |
| Sprint 2 | 2 nov 2026 | TDD, BDD y calidad ágil | Incremento de Proveedores y Compras e Inventario con pruebas unitarias, BDD y cobertura del 100 % | [3-sprint-2](3-sprint-2/acta.md) |
| Sprint 3 | 21 nov 2026 | ERP en Visual Studio: ASP.NET Core MVC con SQL Server | CRUD de los 7 módulos, tablero gerencial, escenarios BDD con Reqnroll y video de demostración | [4-sprint-3](4-sprint-3/acta.md) |
| Sprint 4 | 4 dic 2026 | Despliegue: Docker, Kubernetes y nube | Imagen Docker, Docker Compose, manifiestos de Kubernetes, despliegue en Azure Container Apps y pipeline de CI | [5-sprint-4](5-sprint-4/acta.md) |
| Cierre | 25 nov 2026 | Cierre del proyecto | KuboERP en producción en Azure, revisión del Sprint 4 y retrospectiva final | [6-cierre](6-cierre/acta.md) |

El estado del Product Backlog está en [product-backlog.md](product-backlog.md). El despliegue con Docker,
Kubernetes y Azure se explica en el [manual de despliegue](despliegue/manual-despliegue.md).
