"""Pasos comunes: verifican el mensaje que muestra KuboERP."""
from behave import then


@then('el sistema muestra "{mensaje}"')
def step_sistema_muestra(context, mensaje):
    assert context.mensaje == mensaje, f"Se esperaba '{mensaje}' y se obtuvo '{context.mensaje}'"


@then('el sistema responde "{mensaje}"')
def step_sistema_responde(context, mensaje):
    assert context.mensaje == mensaje, f"Se esperaba '{mensaje}' y se obtuvo '{context.mensaje}'"


@then('el sistema confirma "{mensaje}"')
def step_sistema_confirma(context, mensaje):
    assert context.mensaje == mensaje, f"Se esperaba '{mensaje}' y se obtuvo '{context.mensaje}'"
