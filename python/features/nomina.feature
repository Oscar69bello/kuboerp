# language: es
# Sprint 2 · Motor de nómina (EP06-US04) con parámetros de 2026
Característica: Cálculo de la nómina mensual
  Como jefe de talento humano
  Quiero calcular la nómina del periodo
  Para pagar a tiempo y con los descuentos de ley

  Esquema del escenario: Auxilio de transporte según el salario
    Dado un empleado administrativo con salario base <salario>
    Cuando se calcula la nómina de 30 días
    Entonces el auxilio de transporte es <auxilio>
    Y el descuento de salud es <salud>

    Ejemplos:
      | salario   | auxilio | salud   |
      | 1750905   | 249095  | 70036   |
      | 3501810   | 249095  | 140072  |
      | 3600000   | 0       | 144000  |
