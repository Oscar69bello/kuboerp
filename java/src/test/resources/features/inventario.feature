# language: es
# Taller 4 · Registro de productos, materia prima e insumos (Mockup 3 · Almacén)
Característica: Actualización de stock de material eléctrico
  Como bodeguero de la Bodega Principal
  Quiero registrar entradas y salidas de productos
  Para mantener el stock de seguridad de cables, breakers y luminarias

  Esquema del escenario: Actualizar stock con cantidad válida
    Dado que el producto "<codigo>" tiene stock actual <stock_actual>
    Cuando se registra una entrada de <cantidad> unidades
    Entonces el stock final debe ser <stock_final>
    Y el movimiento queda registrado en el historial

    Ejemplos:
      | codigo       | stock_actual | cantidad | stock_final |
      | CAB-THHN-12  | 10           | 5        | 15          |
      | BRK-2X30     | 0            | 20       | 20          |
      | LED-6060-48W | 50           | 10       | 60          |

  Escenario: Rechazar salida que deja stock negativo
    Dado que el producto "CAB-THHN-12" tiene stock 5
    Cuando se intenta retirar 10 unidades
    Entonces el sistema muestra "Stock insuficiente"
    Y el stock permanece en 5

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
