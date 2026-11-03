"""Taller 4 · Step definitions de inventario."""
from behave import given, then, when

CATALOGO = {
    "CAB-THHN-12": ("Cable THHN 12 AWG (rollo 100 m)", "Cables"),
    "BRK-2X30": ("Breaker 2x30A", "Breakers y tableros"),
    "LED-6060-48W": ("Panel LED 60x60 48W", "Iluminación"),
    "TOMA-DOBLE-PT": ("Toma doble con polo a tierra", "Interruptores y tomas"),
}


@given('que el producto "{codigo}" tiene stock {stock:d}')
def step_producto_con_stock(context, codigo, stock):
    nombre, categoria = CATALOGO.get(codigo, (codigo, "Material eléctrico"))
    context.inventario.register_product(codigo, nombre, categoria, stock)
    context.codigo = codigo


@when('se retiran {cantidad:d} unidades')
def step_se_retiran(context, cantidad):
    context.ejecutar(lambda: context.inventario.retirar(context.codigo, cantidad))


@when('se registra una entrada de {cantidad:d} unidades')
def step_entrada(context, cantidad):
    context.ejecutar(lambda: context.inventario.update_stock(context.codigo, cantidad))


@then('el stock final es {final:d}')
def step_stock_final(context, final):
    assert context.inventario.stock_de(context.codigo) == final
