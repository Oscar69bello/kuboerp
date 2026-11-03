"""Ejercicio práctico 3 y Taller 2 · Step definitions de cotizaciones."""
from behave import given, then, when

from kuboerp.cotizaciones import MSG_REGISTRADA


@given('que existe el proveedor "{nombre}" con NIT "{nit}"')
def step_existe_proveedor(context, nombre, nit):
    context.proveedores.create_supplier(nit, nombre, "ventas@importadoraluzled.com")
    context.nit = nit


@given('que existe una solicitud "{codigo}" en estado "{estado}"')
def step_existe_solicitud(context, codigo, estado):
    context.repo_cotizaciones.add_request(codigo, estado)
    context.solicitud = codigo


@when('el proveedor con NIT "{nit}" cotiza la solicitud "{solicitud}" por {monto:d} con el código "{codigo}"')
def step_cotiza(context, nit, solicitud, monto, codigo):
    def accion():
        context.cotizacion = context.cotizaciones.registrar(codigo, solicitud, nit, monto)
        return MSG_REGISTRADA
    context.ejecutar(accion)


@then('la cotización "{codigo}" queda en estado "{estado}"')
def step_cotizacion_en_estado(context, codigo, estado):
    assert context.cotizacion.codigo == codigo
    assert context.cotizacion.estado == estado


@when('registro una cotización por {monto:d}')
def step_registro_cotizacion(context, monto):
    def accion():
        context.cotizaciones.registrar("COT-0002", context.solicitud, context.nit, monto)
        return MSG_REGISTRADA
    context.ejecutar(accion)


@given('que el proveedor con NIT "{nit}" ya cotizó la solicitud "{solicitud}"')
def step_ya_cotizo(context, nit, solicitud):
    context.cotizaciones.registrar("COT-0001", solicitud, nit, 2300000)
