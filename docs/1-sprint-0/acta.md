# Sprint 0 · "Prepara tu nave"

**Definición y planeación del proyecto ERP** · Entrega: **13 de septiembre de 2026**
Proyecto: *ElectroSoluciones Digital* (desde el Sprint 1, KuboERP) · Responsable: Oscar Javier Bello Daza

## Sprint Planning
**Objetivo del sprint:** pasar de la idea a un proyecto definido con arquitectura, requisitos y plataformas.

**Tareas**
1. Evaluar ventajas y desventajas de desarrollar un ERP en el sector eléctrico.
2. Definir problema, solución, justificación, usuario final y utilidad.
3. Aplicar el modelo 4+1 de Kruchten y elegir el estilo de arquitectura.
4. Especificar el árbol de descomposición funcional, los requisitos no funcionales, el alcance y las tecnologías.
5. Preparar las plataformas de trabajo con herramientas Microsoft, como exige el proyecto.

## Trabajo realizado
- **Modelo 4+1** aplicado: vista lógica (Producto, Proveedor, Empleado, OrdenDeCompra, OrdenDeTrabajo, Factura,
  Cliente), proceso (venta → inventario → factura electrónica DIAN), desarrollo (capas en Visual Studio),
  física (Azure App Service + Azure SQL) y escenarios.
- **Arquitectura en capas con principios de Domain-Driven Design**, presentación en Blazor.
- **Árbol de descomposición funcional** en 6 módulos: Proveedores, Talento Humano, Inventario, Ventas,
  Servicios Técnicos y CRM.
- **Requisitos no funcionales**, alcance (triple restricción) y **stack 100 % Microsoft**: C#, ASP.NET Core,
  Blazor, SQL Server / Azure SQL, Azure DevOps.
- **Presupuesto total** (alcance comercial + ERP interno): **$118.991.000 COP**.
- Ficha técnica del proyecto.

## Sprint Review
Documento del Sprint 0 entregado el 13 de septiembre. El alcance se amplió del canal comercial a un ERP interno
con los módulos de Proveedores, Talento Humano e Inventario.

## Retrospectiva
| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Arquitectura y stack definidos antes de modelar | El nombre del producto (*ElectroSoluciones Digital*) se confundía con el de la empresa | Darle al ERP un nombre propio: **KuboERP** (Sprint 1) |
| Presupuesto actualizado con los módulos nuevos | El repositorio de código aún no tenía incremento | Publicar el código en GitHub cuando exista el primer incremento (Sprint 2) |
