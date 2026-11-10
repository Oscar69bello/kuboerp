"""Sprint 2 · Step definitions de stock crítico y nómina."""
from behave import given, then, when

from kuboerp.inventario import RegistroAlertas
from kuboerp.nomina import MotorNomina
from kuboerp.talento_humano import Administrativo, Novedades


@given('que el producto "{codigo}" tiene stock {stock:d} y stock mínimo {minimo:d}')
def step_producto_con_minimo(context, codigo, stock, minimo):
    context.alertas = RegistroAlertas()
    context.inventario.suscribir(context.alertas)
    context.inventario.register_product(codigo, codigo, "Material eléctrico", stock, minimo)
    context.codigo = codigo


@then('se genera una alerta de stock crítico para "{codigo}"')
def step_alerta(context, codigo):
    assert [a.codigo for a in context.alertas.alertas] == [codigo]


@then('la cantidad sugerida para reponer es {cantidad:d}')
def step_cantidad_sugerida(context, cantidad):
    assert context.alertas.alertas[0].cantidad_sugerida == cantidad


@then('no se genera ninguna alerta')
def step_sin_alerta(context):
    assert context.alertas.alertas == []


@given('un empleado administrativo con salario base {salario:d}')
def step_empleado(context, salario):
    context.empleado = Administrativo("1010203040", "Camila Díaz", "Auxiliar", "FIJO", salario)


@when('se calcula la nómina de {dias:d} días')
def step_calcular(context, dias):
    context.desprendible = MotorNomina().calcular(context.empleado, Novedades(dias_laborados=dias))


@then('el auxilio de transporte es {valor:d}')
def step_auxilio(context, valor):
    assert context.desprendible.auxilio_transporte == valor


@then('el descuento de salud es {valor:d}')
def step_salud(context, valor):
    assert context.desprendible.salud == valor
