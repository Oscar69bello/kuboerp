# language: es
# Ejercicio 4 · Cotizaciones de proveedores (Mockup 3 · Compras)
Característica: Registro de cotizaciones de material eléctrico
  Como jefe de compras
  Quiero registrar las cotizaciones que envían los proveedores
  Para comparar precios antes de generar la orden de compra

  Antecedentes:
    Dado que existe una solicitud de compra "SC-0001" para "Panel LED 60x60 48W" en estado "ABIERTA"

  Escenario: Registrar cotización con monto válido
    Cuando el proveedor con NIT "901555777" registra la cotización "COT-0001" por 2300000
    Entonces el sistema responde "Cotización registrada"

  Escenario: Rechazar cotización con monto cero
    Cuando el proveedor con NIT "901555777" registra la cotización "COT-0002" por 0
    Entonces el sistema muestra "El monto debe ser mayor que cero"
    Y no se registra la cotización
