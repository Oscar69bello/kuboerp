#language: es
# Ejercicio 5 · SpecFlow / Reqnroll en .NET (Mockup 3 · Almacén)
Característica: Registro y retiro de productos en la Bodega Principal de KuboERP
  Como bodeguero
  Quiero registrar productos y retirar unidades del inventario
  Para que el stock nunca quede negativo

  Escenario: Registrar un producto nuevo
    Dado que no existe un producto con código "PINZA-VA-01"
    Cuando registro el producto con código "PINZA-VA-01" y stock inicial 8
    Entonces el producto se crea con estado "DISPONIBLE"

  Escenario: Retirar unidades disponibles
    Dado que el producto "BRK-2X30" tiene stock 40
    Cuando intento retirar 5 unidades
    Entonces el stock queda en 35

  Escenario: Rechazar un retiro mayor al stock disponible
    Dado que el producto "BRK-2X30" tiene stock 2
    Cuando intento retirar 5 unidades
    Entonces se lanza InsufficientStockException
    Y el stock permanece en 2
