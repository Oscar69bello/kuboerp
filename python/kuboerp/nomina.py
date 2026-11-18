"""Motor de nómina mensual (EP06-US04).

Calcula, para cada empleado activo, el devengado, las deducciones, los aportes del empleador y el neto, y
genera un desprendible. Las reglas siguen la normativa colombiana vigente en 2026; los valores están en
ParametrosNomina para actualizarlos cada año sin tocar el motor (SOLID · O).

Reglas implementadas
* Auxilio de transporte para quien devenga hasta 2 SMMLV (Ley 15 de 1959), proporcional a los días.
* Deducciones del trabajador: salud 4 %, pensión 4 % y Fondo de Solidaridad Pensional 1 % desde 4 SMMLV
  (simplificación: no se modelan los puntos adicionales que la ley aplica desde 16 SMMLV).
* Pagos no salariales que superen el 40 % de la remuneración total suman a la base de aportes
  (art. 30 de la Ley 1393 de 2010).
* El ingreso base de cotización (IBC) no puede ser menor que un SMMLV proporcional a los días.
* Aportes del empleador: pensión 12 %, ARL según la clase de riesgo y caja de compensación 4 %. Salud
  (8,5 %), SENA (2 %) e ICBF (3 %) solo para quien devenga 10 SMMLV o más (exoneración, art. 114-1 del
  Estatuto Tributario).
"""
from dataclasses import dataclass, field

from kuboerp.talento_humano import Novedades

TARIFAS_ARL = {1: 0.00522, 2: 0.01044, 3: 0.02436, 4: 0.0435, 5: 0.0696}


@dataclass(frozen=True)
class ParametrosNomina:
    smmlv: int = 1_750_905                 # Decreto 1469 de 2025
    auxilio_transporte: int = 249_095      # Decreto 1470 de 2025
    horas_mensuales: int = 180             # 42 h semanales desde el 15 de julio de 2026 (Ley 2101 de 2021)
    recargo_extra_diurna: float = 0.25
    salud_trabajador: float = 0.04
    pension_trabajador: float = 0.04
    solidaridad_pensional: float = 0.01
    pension_empleador: float = 0.12
    salud_empleador: float = 0.085
    caja_compensacion: float = 0.04
    sena: float = 0.02
    icbf: float = 0.03
    limite_no_salarial: float = 0.40


@dataclass
class Desprendible:
    cedula: str
    nombre: str
    devengado_salarial: int
    auxilio_transporte: int
    devengado_no_salarial: int
    ibc: int
    salud: int
    pension: int
    solidaridad_pensional: int
    aportes_empleador: dict = field(default_factory=dict)

    @property
    def total_devengado(self):
        return self.devengado_salarial + self.auxilio_transporte + self.devengado_no_salarial

    @property
    def total_deducciones(self):
        return self.salud + self.pension + self.solidaridad_pensional

    @property
    def neto(self):
        return self.total_devengado - self.total_deducciones

    @property
    def costo_empleador(self):
        return self.total_devengado + sum(self.aportes_empleador.values())


class MotorNomina:
    def __init__(self, parametros=None):
        self.p = parametros or ParametrosNomina()

    def calcular(self, empleado, novedades=None):
        novedades = novedades or Novedades()
        p = self.p
        salarial = empleado.devengado_salarial(novedades, p)
        no_salarial = empleado.devengado_no_salarial(novedades)
        dias = novedades.dias_laborados

        auxilio = p.auxilio_transporte * dias / 30 if empleado.salario_base <= 2 * p.smmlv else 0
        ibc = self._ibc(salarial, no_salarial, dias)

        salud = ibc * p.salud_trabajador
        pension = ibc * p.pension_trabajador
        fsp = ibc * p.solidaridad_pensional if ibc >= 4 * p.smmlv else 0

        return Desprendible(
            cedula=empleado.cedula, nombre=empleado.nombre,
            devengado_salarial=round(salarial), auxilio_transporte=round(auxilio),
            devengado_no_salarial=round(no_salarial), ibc=round(ibc),
            salud=round(salud), pension=round(pension), solidaridad_pensional=round(fsp),
            aportes_empleador=self._aportes_empleador(empleado, salarial, ibc))

    def liquidar_periodo(self, empleados, novedades_por_cedula=None):
        """Desprendibles de todos los empleados activos del periodo."""
        novedades_por_cedula = novedades_por_cedula or {}
        return [self.calcular(e, novedades_por_cedula.get(e.cedula)) for e in empleados
                if e.estado == "ACTIVO"]

    @staticmethod
    def resumen(desprendibles):
        return {
            "empleados": len(desprendibles),
            "total_devengado": sum(d.total_devengado for d in desprendibles),
            "total_deducciones": sum(d.total_deducciones for d in desprendibles),
            "total_neto": sum(d.neto for d in desprendibles),
            "costo_empleador": sum(d.costo_empleador for d in desprendibles),
        }

    def _ibc(self, salarial, no_salarial, dias):
        p = self.p
        exceso = max(0.0, no_salarial - p.limite_no_salarial * (salarial + no_salarial))
        return max(salarial + exceso, p.smmlv * dias / 30)

    def _aportes_empleador(self, empleado, salarial, ibc):
        p = self.p
        aportes = {
            "pension": ibc * p.pension_empleador,
            "arl": ibc * TARIFAS_ARL[empleado.nivel_riesgo_arl],
            "caja_compensacion": ibc * p.caja_compensacion,
        }
        if salarial >= 10 * p.smmlv:
            aportes.update(salud=ibc * p.salud_empleador, sena=ibc * p.sena, icbf=ibc * p.icbf)
        return {concepto: round(valor) for concepto, valor in aportes.items()}
