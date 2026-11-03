# Sprint 2 · TDD, BDD y calidad ágil

**Primer incremento de código con pruebas** · Entrega: **2 de noviembre de 2026**
Responsable: Oscar Javier Bello Daza

## Sprint Planning
**Objetivo del sprint:** construir el incremento de Proveedores y Compras e Inventario de KuboERP aplicando
pruebas desde el primer minuto.

**Historias del sprint:** EP05-US01, EP05-US04, EP05-US05, EP05-US06, EP05-US07 (nueva: cotizaciones de
proveedores), EP07-US03 y EP01-US04. Ver [product-backlog.md](../product-backlog.md).

**Tareas**
1. Taller de herramientas de prueba: Gherkin, JUnit 5, Jest, Cucumber, SpecFlow y Font Awesome.
2. Taller de TDD, BDD y calidad ágil con Python en Google Colab.
3. Medir la cobertura y superar el 80 % que exige la Definition of Done.
4. Publicar el incremento en GitHub.

## Trabajo realizado
| Fecha | Trabajo | Resultado |
|---|---|---|
| 25 oct | Taller de herramientas de prueba en Java, JavaScript y .NET | 37 pruebas JUnit 5 + Cucumber, 15 de Jest y 3 escenarios de SpecFlow (Reqnroll), todas aprobadas |
| 2 nov | Taller de TDD/BDD con Python en Google Colab | Ciclo Rojo → Verde → Refactor de `update_stock`; 27 pruebas unitarias, 20 escenarios de Behave; cobertura de 92 % a 100 % |
| 2 nov | Repositorio | Incremento publicado en https://github.com/Oscar69bello/kuboerp |

## Sprint Review
**Criterios de aceptación cumplidos:** NIT único y válido, desactivación de proveedores sin órdenes activas,
cotizaciones solo sobre solicitudes abiertas y con monto mayor que cero, aprobación de órdenes dentro del
presupuesto y sin doble aprobación, y bloqueo de retiros mayores al stock.

**Definition of Done:**
| Criterio | Estado |
|---|---|
| Pruebas unitarias en verde y cobertura ≥ 80 % | ✔ 100 % (coverage.py) |
| Criterios de aceptación cubiertos por escenarios BDD | ✔ 19 escenarios Cucumber y 20 de Behave |
| Código versionado en GitHub | ✔ |
| Revisión por pull request de un compañero | ✘ El trabajo fue individual |
| Pruebas en xUnit, API en Swagger y despliegue en Azure | ✘ El taller pedía Python, Java, JavaScript y .NET con SpecFlow; quedan para los sprints de desarrollo |

## Retrospectiva
| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Los criterios Dado/Cuando/Entonces del backlog se convirtieron directamente en escenarios BDD | En Windows, las rutas largas impidieron compilar | Trabajar en una ruta corta (`C:\KuboERP`) |
| La cobertura mostró que la regla de NIT duplicado solo la probaba un escenario BDD | `JAVA_HOME` apuntaba a un JRE y Maven no compilaba | Configurar el JDK 25 en IntelliJ |
| Las pruebas dieron el mismo resultado en local y en Colab | Al ejecutar el notebook dos veces, la cobertura inicial salía en 100 % | Reiniciar el entorno de Colab antes de cada ejecución completa |
| — | SpecFlow fue retirado en 2024 | Usar su sucesor, Reqnroll |
| — | No se pudo crear la organización de Azure DevOps: la cuenta personal quedó bloqueada por Microsoft y la institucional exige una suscripción de Azure | Llevar el tablero en GitHub Projects (también de Microsoft) y evaluar Azure for Students para los siguientes sprints |

## Herramienta de seguimiento
El tablero del proyecto está en **GitHub Projects** (*KuboERP · Scrum*), ligado al repositorio: cada iteración es un
*milestone* y cada historia o tarea es un *issue*. La Definition of Done del Sprint 1 nombraba Azure Boards; se
cambió por el impedimento descrito en la retrospectiva.
