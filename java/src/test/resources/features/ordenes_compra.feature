# language: es
# Taller 3 · Aprobación de Órdenes de Compra (Mockup 3 · Compras)
Característica: Aprobación de órdenes de compra contra el presupuesto del proveedor
  Como jefe de compras
  Quiero aprobar las órdenes de compra sin exceder el presupuesto de cada proveedor
  Para controlar el gasto en material eléctrico

  Antecedentes:
    Dado que el proveedor "Distribuidora Eléctrica del Centro" tiene presupuesto disponible de $10.000.000

  Escenario: Aprobar orden dentro del presupuesto
    Dado que existe una orden "OC-0001" por $5.000.000 en estado "PENDIENTE"
    Cuando el jefe de compras aprueba la orden
    Entonces la orden cambia a "APROBADA"
    Y el presupuesto del proveedor se reduce a $5.000.000

  Escenario: Rechazar orden que excede el presupuesto
    Dado que existe una orden "OC-0002" por $15.000.000 en estado "PENDIENTE"
    Cuando el jefe de compras aprueba la orden
    Entonces el sistema muestra "Presupuesto insuficiente"
    Y la orden permanece en "PENDIENTE"
    Y el presupuesto disponible del proveedor sigue en $10.000.000

  Escenario: No volver a aprobar una orden ya aprobada
    Dado que existe una orden "OC-0003" por $1.000.000 en estado "APROBADA"
    Cuando el jefe de compras aprueba la orden
    Entonces el sistema muestra "La orden ya está aprobada"
