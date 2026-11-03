"""Taller 1 · Step definitions de proveedores."""
from behave import given, then, when

from kuboerp.ordenes import PurchaseOrder
from kuboerp.proveedores import MSG_REGISTRADO


@given('que no existe un proveedor con NIT "{nit}"')
def step_no_existe_proveedor(context, nit):
    assert not context.proveedores.existe_por_nit(nit)


@when('registro el proveedor con NIT "{nit}", nombre "{nombre}" y correo "{correo}"')
def step_registro_proveedor(context, nit, nombre, correo):
    def accion():
        context.proveedor = context.proveedores.create_supplier(nit, nombre, correo)
        return MSG_REGISTRADO
    context.ejecutar(accion)


@then('el proveedor se crea con estado "{estado}"')
def step_proveedor_creado(context, estado):
    assert context.proveedor is not None
    assert context.proveedor.estado == estado


@given('que ya existe un proveedor con NIT "{nit}"')
def step_ya_existe_proveedor(context, nit):
    context.proveedores.create_supplier(nit, "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co")
    context.nit = nit
    context.proveedores_antes = context.repo_proveedores.count()


@when('intento registrar otro proveedor con el mismo NIT')
def step_registro_duplicado(context):
    context.ejecutar(lambda: context.proveedores.create_supplier(
        context.nit, "Schneider Electric Colombia", "ventas@schneider.com.co"))


@then('no se crea un nuevo proveedor')
def step_no_se_crea(context):
    assert context.repo_proveedores.count() == context.proveedores_antes


@when('registro un proveedor con correo "{correo}"')
def step_registro_con_correo(context, correo):
    def accion():
        context.proveedores.create_supplier("901555777", "Importadora LuzLED", correo)
        return "Correo válido"
    context.ejecutar(accion)


@given('que existe un proveedor "{nombre}" con NIT "{nit}" sin órdenes de compra activas')
def step_proveedor_sin_ordenes(context, nombre, nit):
    context.proveedores.create_supplier(nit, nombre, "contacto@proveedor.com.co")
    context.nit = nit
    assert not context.repo_ordenes.has_active_orders(nit)


@given('que existe un proveedor "{nombre}" con NIT "{nit}" y la orden de compra "{orden}" en estado "{estado}"')
def step_proveedor_con_orden(context, nombre, nit, orden, estado):
    context.proveedores.create_supplier(nit, nombre, "contacto@proveedor.com.co")
    context.repo_ordenes.save(PurchaseOrder(orden, nit, 3_000_000, estado))
    context.nit = nit


@when('solicito eliminar el proveedor')
def step_eliminar_proveedor(context):
    context.ejecutar(lambda: context.proveedores.delete_supplier(context.nit))


@then('el proveedor cambia a estado "{estado}"')
def step_proveedor_cambia_estado(context, estado):
    assert context.proveedores.buscar(context.nit).estado == estado


@then('el proveedor sigue en estado "{estado}"')
def step_proveedor_sigue_estado(context, estado):
    assert context.proveedores.buscar(context.nit).estado == estado
