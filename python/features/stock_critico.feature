# language: es
# Sprint 2 · Control de stock crítico (EP07-US02 · política P04 del Event Storming)
Característica: Alertas de stock crítico en la Bodega Principal
  Como administrador de inventario
  Quiero recibir una alerta cuando un material llega a su stock mínimo
  Para generar la orden de compra antes de quedarme sin existencias

  Escenario: Un retiro deja el cable en su stock mínimo
    Dado que el producto "CAB-THHN-12" tiene stock 30 y stock mínimo 10
    Cuando se retiran 20 unidades
    Entonces se genera una alerta de stock crítico para "CAB-THHN-12"
    Y la cantidad sugerida para reponer es 10

  Escenario: Un retiro que no llega al mínimo no genera alerta
    Dado que el producto "BRK-2X30" tiene stock 40 y stock mínimo 15
    Cuando se retiran 5 unidades
    Entonces no se genera ninguna alerta
