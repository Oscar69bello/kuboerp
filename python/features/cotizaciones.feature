# language: es
# Ejercicio práctico 3 y Taller 2 · Cotizaciones de proveedores (Mockup 3 · Compras)
Característica: Registro de cotizaciones de material eléctrico
  Como jefe de compras
  Quiero registrar las cotizaciones que envían los proveedores
  Para comparar precios antes de generar la orden de compra

  Antecedentes:
    Dado que existe el proveedor "Importadora LuzLED" con NIT "901555777"
    Y que existe una solicitud "SC-0001" en estado "ABIERTA"

  Escenario: Registrar la cotización de un proveedor
    Cuando el proveedor con NIT "901555777" cotiza la solicitud "SC-0001" por 2300000 con el código "COT-0001"
    Entonces la cotización "COT-0001" queda en estado "RECIBIDA"
    Y el sistema responde "Cotización registrada"

  Esquema del escenario: Validar monto de cotización
    Cuando registro una cotización por <monto>
    Entonces el sistema responde "<resultado>"

    Ejemplos:
      | monto   | resultado             |
      | 2500000 | Cotización registrada |
      | 0       | Monto inválido        |
      | -1000   | Monto inválido        |

  Escenario: Rechazar una segunda cotización del mismo proveedor
    Dado que el proveedor con NIT "901555777" ya cotizó la solicitud "SC-0001"
    Cuando registro una cotización por 2500000
    Entonces el sistema responde "El proveedor ya cotizó esta solicitud"
