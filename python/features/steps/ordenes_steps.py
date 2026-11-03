"""Taller 3 · Step definitions de la aprobación de órdenes de compra."""
import parse
from behave import given, register_type, then, when

from kuboerp.ordenes import PurchaseOrder
from kuboerp.proveedores import Supplier

NIT_PROVEEDOR = "900123456"


@parse.with_pattern(r"\$[\d.]+")
def parse_pesos(texto):
    """Convierte "$10.000.000" en 10000000."""
    return int(texto.replace("$", "").replace(".", ""))


register_type(Pesos=parse_pesos)


@given('que el proveedor "{nombre}" tiene presupuesto disponible de {presupuesto:Pesos}')
def step_presupuesto_proveedor(context, nombre, presupuesto):
    context.repo_proveedores.save(
        Supplier(NIT_PROVEEDOR, nombre, "compras@electrocentro.com.co", presupuesto=presupuesto))


@given('que existe una orden "{codigo}" por {monto:Pesos} en estado "{estado}"')
def step_existe_orden(context, codigo, monto, estado):
    context.repo_ordenes.save(PurchaseOrder(codigo, NIT_PROVEEDOR, monto, estado))
    context.codigo_orden = codigo


@when('el jefe de compras aprueba la orden')
def step_aprueba_orden(context):
    def accion():
        context.ordenes.approve(context.codigo_orden)
        return "Orden aprobada"
    context.ejecutar(accion)


@then('la orden cambia a "{estado}"')
def step_orden_cambia(context, estado):
    assert context.repo_ordenes.find_by_codigo(context.codigo_orden).estado == estado


@then('la orden permanece en "{estado}"')
def step_orden_permanece(context, estado):
    assert context.repo_ordenes.find_by_codigo(context.codigo_orden).estado == estado


@then('el presupuesto del proveedor se reduce a {esperado:Pesos}')
def step_presupuesto_reducido(context, esperado):
    # Se consulta el presupuesto actualizado en el repositorio y se compara con el esperado.
    actual = context.repo_proveedores.find_by_nit(NIT_PROVEEDOR).presupuesto
    assert actual == esperado, f"Presupuesto esperado {esperado}, actual {actual}"


@then('el presupuesto disponible del proveedor sigue en {esperado:Pesos}')
def step_presupuesto_sin_cambio(context, esperado):
    actual = context.repo_proveedores.find_by_nit(NIT_PROVEEDOR).presupuesto
    assert actual == esperado, f"Presupuesto esperado {esperado}, actual {actual}"
