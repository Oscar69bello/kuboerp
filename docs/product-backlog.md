# Product Backlog · KuboERP

| Versión | Iteración | Contenido |
|---|---|---|
| 1 | Inicio (6 sep) | 4 épicas y 16 historias, priorizadas con MoSCoW y estimadas con Planning Poker: **97 SP** ([Excel](0-inicio/ElectroSolutions_Epics_User_Stories.xlsx)) |
| 2 | Sprint 1 (12 oct) | Refinamiento: 7 épicas y **41 historias (212 SP)**, repartidas en 9 sprints de desarrollo. Se agregan las historias CRUD faltantes y tres épicas para el ERP interno |

## Épicas

| ID | Épica | Origen |
|---|---|---|
| EP01 | Catálogo y compra de materiales eléctricos | Inicio |
| EP02 | Servicios técnicos | Inicio |
| EP03 | Clientes y administración | Inicio |
| EP04 | Garantías y posventa | Inicio |
| EP05 | Proveedores y compras | Sprint 1 |
| EP06 | Talento humano | Sprint 1 |
| EP07 | Inventario y bodega | Sprint 1 |

## Historias trabajadas en el Sprint 2 (incremento con pruebas)

El taller de pruebas pedía cubrir proveedores, cotizaciones, órdenes de compra e inventario, así que el Product
Owner adelantó historias de EP05 y EP07 que estaban planeadas para los sprints de desarrollo 6 a 8.

| ID | Historia | Alcance implementado y probado | Estado |
|---|---|---|---|
| EP05-US01 | Registrar proveedores | NIT único y válido, correo válido, nombre obligatorio | **Hecho** |
| EP05-US04 | Desactivar proveedores | Borrado lógico (INACTIVO); no se desactiva si tiene órdenes activas | **Hecho** |
| EP05-US05 | Crear órdenes de compra | Orden a un proveedor con monto y estado PENDIENTE | **Hecho** (parcial: sin detalle de productos) |
| EP05-US06 | Aprobar, recibir o cancelar una orden de compra | Aprobación contra el presupuesto del proveedor, sin doble aprobación | **Hecho** (parcial: aprobación) |
| EP05-US07 *(nueva)* | Registrar cotizaciones de proveedores | Solo sobre solicitudes ABIERTAS, monto > 0, una por proveedor; estado RECIBIDA | **Hecho** |
| EP07-US03 | Registrar entradas y salidas de inventario | Entradas y retiros con kardex; no se retira más del stock disponible | **Hecho** (sin traslados entre bodegas) |
| EP01-US04 | Gestión y actualización de stock | Registro de productos con código único, stock ≥ 0 y categoría obligatoria | **Hecho** (sin carga masiva ni alertas) |

Las demás historias siguen en el backlog para los sprints de desarrollo planeados.
