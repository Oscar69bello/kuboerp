# Sprint 3 · ERP en Visual Studio: ASP.NET Core MVC con SQL Server

**Del dominio probado a la aplicación web** · 10 al 21 de noviembre de 2026
Responsable: Oscar Javier Bello Daza (Product Owner, Scrum Master y equipo de desarrollo)

## Sprint Planning
**Objetivo del sprint:** llevar las reglas de negocio probadas en Python a una aplicación web en el stack del
proyecto (C#, ASP.NET Core y SQL Server), con interfaz CRUD para cada módulo y un tablero gerencial.

| Historia | Alcance del sprint |
|---|---|
| EP05-US01, US02, US04 | CRUD de proveedores con NIT único, desactivación lógica y reactivación |
| EP05-US07 | Solicitudes y cotizaciones; selección de la ganadora |
| EP05-US05, US06 | Órdenes de compra con líneas, aprobación contra presupuesto, recepción y cancelación con auditoría |
| EP01-US04, EP07-US02, US03, US04 | Inventario con kardex, stock mínimo y alerta de stock crítico |
| EP06-US01 a US04 | Empleados, contratos y liquidación de nómina con parámetros 2026 |
| EP03-US01 *(parcial)* | Tablero gerencial con indicadores de compras, inventario y nómina |

**Tareas:** solución `KuboERP.slnx` (.NET 10), modelo con Entity Framework Core y SQL Server LocalDB, servicios de
dominio, controladores y vistas Razor, datos de ejemplo de ElectroSoluciones S.A.S., escenarios BDD con Reqnroll,
guion y video de demostración en Teams.

## Trabajo realizado
| Fecha | Trabajo | Resultado |
|---|---|---|
| 18–20 nov | Modelo de datos (10 entidades) y servicios de dominio | Reglas de negocio iguales a las del dominio en Python |
| 20–21 nov | Controladores y vistas de los 7 módulos | CRUD completo y tablero gerencial |
| 21 nov | Perfiles de ejecución (http, IIS Express, reinicio de datos) | La app abre en Visual Studio sin certificado local |
| 21 nov | Video de demostración en Microsoft Teams | Recorrido de 16 min por Visual Studio y la aplicación |

## Sprint Review
El Product Owner aceptó el CRUD de los módulos y el tablero. Quedó pendiente publicar la aplicación fuera del
equipo local: LocalDB solo existe en Windows con Visual Studio.

## Retrospectiva
| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Reutilizar las reglas ya probadas en Python aceleró el desarrollo | El certificado HTTPS de desarrollo bloqueaba la ejecución | Perfil http en desarrollo; https solo en producción |
| Los datos de ejemplo permiten demostrar sin preparar nada | La aplicación depende de LocalDB | Sprint 4: contenedores y base de datos en la nube |
