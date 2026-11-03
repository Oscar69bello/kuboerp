# Sprint 1 · Diseño y especificación del ERP

**Del plano del ERP al prototipo con PlantUML y Figma** · Entrega: **12 de octubre de 2026**
(documento de diseño y especificación y video de Figma sobre el funcionamiento de los CRUD)
Responsable: Oscar Javier Bello Daza

## Sprint Planning
**Objetivo del sprint:** llevar el ERP de los requerimientos a un prototipo funcional, con nombre e identidad propios.

**Tareas**
1. Renombrar el producto a **KuboERP** y definir su identidad visual (cubo con la K, paleta azul,
   lema *Automatiza • Integra • Optimiza*).
2. Usar el Event Storming para dar trazabilidad a los requerimientos.
3. Especificar requerimientos funcionales (IEEE 830) y no funcionales (ISO/IEC 25010).
4. Refinar el Product Backlog con las historias CRUD faltantes y definir la Definition of Done.
5. Modelar con PlantUML en Google Colab: casos de uso, clases, entidad-relación, árbol de descomposición y C4.
6. Diseñar el sistema de diseño y los mockups, escribir los prompts de Figma Make y grabar el video de los CRUD.

## Trabajo realizado
- **Event Storming:** 69 eventos de dominio, 30 políticas, 12 *hotspots* y 7 *bounded contexts*.
- **36 requerimientos funcionales** con operación CRUD, actor y criterio de aceptación, y **17 no funcionales**.
- **Backlog refinado:** 7 épicas (nuevas: EP05 Proveedores y compras, EP06 Talento humano, EP07 Inventario y bodega)
  y **41 historias (212 SP)** repartidas en 9 sprints de desarrollo.
- **Definition of Done** adaptada al ecosistema Microsoft: revisión por pull request, pruebas unitarias con
  cobertura ≥ 80 %, documentación de API y arquitectura, despliegue en Azure y aceptación del Product Owner.
- **Diagramas PlantUML** en Google Colab (casos de uso, clases, entidad-relación, WBS y C4 de contexto).
- **Mockups** de Compras, Inventario y Nómina, y **prompts de Figma Make** para 4 prototipos dinámicos con CRUD:
  Dirección y Finanzas, Comercial y Ventas, Compras, Logística y Almacén, y Operaciones, SST y Posventa.
- **Guion y presentación del video** y **Video Figma** del funcionamiento de los CRUD (12 oct).

## Sprint Review
El prototipo muestra el CRUD completo por módulo y la integración entre módulos (una venta descuenta inventario,
una cotización aprobada se convierte en pedido). El módulo de Proveedores, Compras e Inventario quedó como
candidato para el primer incremento de código.

## Retrospectiva
| ¿Qué salió bien? | ¿Qué mejorar? | Acción |
|---|---|---|
| Trazabilidad completa: evento → requerimiento → historia | Figma Make limita los prompts a 2.000 palabras | Un prompt por módulo |
| Identidad visual única en todos los artefactos | Los mockups no validan las reglas de negocio | Implementar las reglas con pruebas unitarias (Sprint 2) |
