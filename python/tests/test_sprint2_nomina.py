"""Sprint 2 · CRUD de empleados y motor de nómina (pytest).

Los valores esperados se calcularon a mano con los parámetros de 2026:
SMMLV $1.750.905 (Decreto 1469 de 2025) y auxilio de transporte $249.095 (Decreto 1470 de 2025).
"""
from datetime import date

import pytest

from kuboerp.excepciones import InvalidEmployeeException
from kuboerp.nomina import MotorNomina, ParametrosNomina
from kuboerp.talento_humano import (Administrativo, Empleado, EmployeeService, Gerente, Novedades,
                                    Tecnico, Vendedor)

SMMLV = 1_750_905


@pytest.fixture
def motor():
    return MotorNomina()


def tecnico():
    return Tecnico("1072345678", "Julián Rojas", "Técnico electricista", "INDEFINIDO", 2_200_000)


# ---------------------------------------------------------------- motor de nómina
def test_tecnico_con_horas_extra_y_auxilio_de_transporte(motor):
    d = motor.calcular(tecnico(), Novedades(horas_extra_diurnas=10))

    # valor hora = 2.200.000 / 180 = 12.222,22 ; 10 h x 12.222,22 x 1,25 = 152.777,78
    assert d.devengado_salarial == 2_352_778
    assert d.auxilio_transporte == 249_095
    assert d.salud == d.pension == 94_111
    assert d.solidaridad_pensional == 0
    assert d.neto == 2_352_778 + 249_095 - 188_222
    assert d.aportes_empleador == {"pension": 282_333, "arl": 102_346, "caja_compensacion": 94_111}


def test_vendedor_comision_es_salario(motor):
    vendedor = Vendedor("52987654", "Laura Gómez", "Asesora comercial", "FIJO", SMMLV,
                        porcentaje_comision=0.02)
    d = motor.calcular(vendedor, Novedades(ventas=10_000_000))
    assert d.devengado_salarial == SMMLV + 200_000
    assert d.ibc == SMMLV + 200_000


def test_gerente_bonificacion_no_salarial_y_limite_del_40(motor):
    gerente = Gerente("79123456", "Andrea Castro", "Gerente comercial", "INDEFINIDO", 12_000_000)
    d = motor.calcular(gerente, Novedades(bonificacion=9_000_000))

    # 40 % de 21.000.000 = 8.400.000 → el exceso de 600.000 suma al IBC
    assert d.devengado_no_salarial == 9_000_000
    assert d.ibc == 12_600_000
    assert d.auxilio_transporte == 0                 # devenga más de 2 SMMLV
    assert d.solidaridad_pensional == 126_000        # IBC ≥ 4 SMMLV
    assert "salud" not in d.aportes_empleador        # < 10 SMMLV: empleador exonerado


def test_salario_de_10_smmlv_o_mas_paga_salud_sena_e_icbf(motor):
    gerente = Gerente("79123456", "Andrea Castro", "Gerente general", "INDEFINIDO", 20_000_000)
    aportes = motor.calcular(gerente).aportes_empleador
    assert aportes["salud"] == 1_700_000
    assert aportes["sena"] == 400_000
    assert aportes["icbf"] == 600_000


def test_dias_laborados_proporcionales(motor):
    admin = Administrativo("1010203040", "Camila Díaz", "Auxiliar contable", "OBRA_LABOR", 2_000_000)
    d = motor.calcular(admin, Novedades(dias_laborados=15))
    assert d.devengado_salarial == 1_000_000
    assert d.auxilio_transporte == 124_548


def test_ibc_no_puede_ser_menor_que_un_smmlv(motor):
    medio_tiempo = Administrativo("1010203041", "Pedro Ruiz", "Mensajero", "FIJO", 1_500_000)
    assert motor.calcular(medio_tiempo).ibc == SMMLV


def test_parametros_configurables_sin_cambiar_el_motor():
    motor_2025 = MotorNomina(ParametrosNomina(smmlv=1_423_500, auxilio_transporte=200_000))
    assert motor_2025.calcular(tecnico()).auxilio_transporte == 200_000


def test_liquidar_periodo_omite_inactivos_y_resume(motor):
    activo = tecnico()
    inactivo = Administrativo("1010203040", "Camila Díaz", "Auxiliar contable", "FIJO", 2_000_000,
                              estado="INACTIVO")
    desprendibles = motor.liquidar_periodo([activo, inactivo], {activo.cedula: Novedades()})

    resumen = MotorNomina.resumen(desprendibles)
    assert resumen["empleados"] == 1
    assert resumen["total_neto"] == desprendibles[0].neto
    assert resumen["costo_empleador"] > resumen["total_devengado"]


def test_empleado_es_abstracto():
    with pytest.raises(TypeError):
        Empleado("1", "x", "y", "FIJO", SMMLV)


# ---------------------------------------------------------------- CRUD de empleados
@pytest.fixture
def servicio():
    servicio = EmployeeService()
    servicio.registrar(tecnico())
    return servicio


@pytest.mark.parametrize("empleado, mensaje", [
    (Tecnico("10A", "Ana", "Técnica", "FIJO", SMMLV), "Cédula inválida"),
    (Tecnico("1099", "", "Técnica", "FIJO", SMMLV), "obligatorios"),
    (Tecnico("1099", "Ana", "Técnica", "PRESTACION", SMMLV), "Tipo de contrato inválido"),
    (Tecnico("1099", "Ana", "Técnica", "FIJO", -1), "no puede ser negativo"),
    (Tecnico("1099", "Ana", "Técnica", "FIJO", 1_000_000), "inferior al salario mínimo"),
    (Tecnico("1072345678", "Ana", "Técnica", "FIJO", SMMLV), "La cédula ya está registrada"),
])
def test_registrar_con_datos_invalidos(servicio, empleado, mensaje):
    with pytest.raises(InvalidEmployeeException, match=mensaje):
        servicio.registrar(empleado)


def test_listar_por_cargo_contrato_y_estado(servicio):
    servicio.registrar(Vendedor("52987654", "Laura Gómez", "Asesora comercial", "FIJO", SMMLV))
    assert len(servicio.listar()) == 2
    assert [e.cedula for e in servicio.listar(cargo="Asesora comercial")] == ["52987654"]
    assert [e.cedula for e in servicio.listar(tipo_contrato="INDEFINIDO")] == ["1072345678"]


def test_actualizar_contrato_conserva_la_version_anterior(servicio):
    empleado = servicio.actualizar_contrato("1072345678", "jefe.th", salario_base=2_500_000,
                                            cargo="Supervisor de campo", fecha=date(2026, 11, 9))
    assert empleado.salario_base == 2_500_000
    assert empleado.cargo == "Supervisor de campo"
    assert empleado.historial == [{"fecha": date(2026, 11, 9), "usuario": "jefe.th",
                                   "salario_base": 2_200_000, "cargo": "Técnico electricista"}]


def test_actualizar_contrato_con_salario_invalido(servicio):
    with pytest.raises(InvalidEmployeeException):
        servicio.actualizar_contrato("1072345678", "jefe.th", salario_base=-5)
    assert servicio.buscar("1072345678").historial == []


def test_desvincular(servicio):
    assert servicio.desvincular("1072345678") == "Empleado desvinculado"
    assert servicio.listar() == []
    assert len(servicio.listar(estado=None)) == 1
    with pytest.raises(InvalidEmployeeException, match="ya está desvinculado"):
        servicio.desvincular("1072345678")
    with pytest.raises(InvalidEmployeeException, match="Empleado no encontrado"):
        servicio.buscar("000")
