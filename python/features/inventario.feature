# language: es
# Taller 4 y Ejercicio práctico 1 · Inventario de la Bodega Principal (Mockup 3 · Almacén)
Característica: Entradas y retiros de material eléctrico
  Como bodeguero de la Bodega Principal
  Quiero registrar entradas y retiros de productos
  Para mantener el stock de seguridad de cables, breakers y luminarias

  Esquema del escenario: Retiro de inventario
    Dado que el producto "<codigo>" tiene stock <stock>
    Cuando se retiran <retiro> unidades
    Entonces el stock final es <final>
    Y el sistema responde "<mensaje>"

    Ejemplos:
      | codigo        | stock | retiro | final | mensaje            |
      | CAB-THHN-12   | 10    | 3      | 7     | Retiro exitoso     |
      | BRK-2X30      | 5     | 5      | 0     | Retiro exitoso     |
      | TOMA-DOBLE-PT | 2     | 5      | 2     | Stock insuficiente |

  Escenario: Registrar una entrada de mercancía
    Dado que el producto "BRK-2X30" tiene stock 40
    Cuando se registra una entrada de 10 unidades
    Entonces el stock final es 50

  Escenario: Rechazar una salida que deja el stock negativo
    Dado que el producto "TOMA-DOBLE-PT" tiene stock 2
    Cuando se retiran 5 unidades
    Entonces el sistema muestra "Stock insuficiente"
    Y el stock final es 2
