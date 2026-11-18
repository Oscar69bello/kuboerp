"""CRUD de empleados (EP06-US01, EP06-US02, EP06-US03, EP06-US05).

Retoma la jerarquía del taller de Herencia y del diagrama de clases del Sprint 1: Empleado es abstracta y
cada tipo de empleado define su propio devengado (polimorfismo). El motor de nómina trabaja con
cualquier Empleado sin preguntar su tipo (SOLID · L: toda subclase puede reemplazar a la base).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date

from kuboerp.excepciones import InvalidEmployeeException

TIPOS_CONTRATO = ("INDEFINIDO", "FIJO", "OBRA_LABOR")
MSG_DESVINCULADO = "Empleado desvinculado"


@dataclass
class Novedades:
    """Novedades del periodo (mes) que reporta el jefe inmediato."""
    dias_laborados: int = 30
    horas_extra_diurnas: float = 0
    ventas: int = 0
    bonificacion: int = 0


@dataclass
class Empleado(ABC):
    cedula: str
    nombre: str
    cargo: str
    tipo_contrato: str
    salario_base: int
    estado: str = "ACTIVO"
    historial: list = field(default_factory=list)

    #: Clase de riesgo ARL (Decreto 1295 de 1994): 1 = mínimo ... 5 = máximo.
    nivel_riesgo_arl = 1

    def salario_proporcional(self, novedades):
        return self.salario_base * novedades.dias_laborados / 30

    @abstractmethod
    def devengado_salarial(self, novedades, parametros):
        """Pagos que constituyen salario (base de aportes y prestaciones)."""

    def devengado_no_salarial(self, novedades):
        """Pagos que no constituyen salario (art. 128 del Código Sustantivo del Trabajo)."""
        return 0


@dataclass
class Tecnico(Empleado):
    """Técnico electricista de campo: cobra horas extra diurnas con recargo del 25 %."""
    nivel_riesgo_arl = 4

    def devengado_salarial(self, novedades, parametros):
        valor_hora = self.salario_base / parametros.horas_mensuales
        extras = novedades.horas_extra_diurnas * valor_hora * (1 + parametros.recargo_extra_diurna)
        return self.salario_proporcional(novedades) + extras


@dataclass
class Vendedor(Empleado):
    """Asesor comercial: salario base más comisión sobre las ventas del periodo (es salario)."""
    porcentaje_comision: float = 0.02

    def devengado_salarial(self, novedades, parametros):
        return self.salario_proporcional(novedades) + novedades.ventas * self.porcentaje_comision


@dataclass
class Gerente(Empleado):
    """Gerente: salario base y bonificación por resultados pactada como no salarial."""

    def devengado_salarial(self, novedades, parametros):
        return self.salario_proporcional(novedades)

    def devengado_no_salarial(self, novedades):
        return novedades.bonificacion


@dataclass
class Administrativo(Empleado):
    def devengado_salarial(self, novedades, parametros):
        return self.salario_proporcional(novedades)


class InMemoryEmployeeRepository:
    def __init__(self):
        self._datos = {}

    def save(self, empleado):
        self._datos[empleado.cedula] = empleado
        return empleado

    def find_by_cedula(self, cedula):
        return self._datos.get(cedula)

    def find_all(self):
        return list(self._datos.values())


class EmployeeService:
    def __init__(self, repo=None, smmlv=1_750_905):
        self.repo = repo if repo is not None else InMemoryEmployeeRepository()
        self.smmlv = smmlv

    # ---------- C ----------
    def registrar(self, empleado):
        if not empleado.cedula or not empleado.cedula.isdigit():
            raise InvalidEmployeeException("Cédula inválida")
        if not empleado.nombre or not empleado.cargo:
            raise InvalidEmployeeException("Nombre y cargo son obligatorios")
        if empleado.tipo_contrato not in TIPOS_CONTRATO:
            raise InvalidEmployeeException("Tipo de contrato inválido")
        self._validar_salario(empleado.salario_base)
        if self.repo.find_by_cedula(empleado.cedula) is not None:
            raise InvalidEmployeeException("La cédula ya está registrada")
        return self.repo.save(empleado)

    # ---------- R ----------
    def buscar(self, cedula):
        empleado = self.repo.find_by_cedula(cedula)
        if empleado is None:
            raise InvalidEmployeeException("Empleado no encontrado")
        return empleado

    def listar(self, cargo=None, tipo_contrato=None, estado="ACTIVO"):
        return [e for e in self.repo.find_all()
                if (cargo is None or e.cargo == cargo)
                and (tipo_contrato is None or e.tipo_contrato == tipo_contrato)
                and (estado is None or e.estado == estado)]

    # ---------- U ----------
    def actualizar_contrato(self, cedula, usuario, salario_base=None, cargo=None, fecha=None):
        """Cambia salario o cargo y conserva la versión anterior con fecha y usuario responsable."""
        empleado = self.buscar(cedula)
        if salario_base is not None:
            self._validar_salario(salario_base)
        empleado.historial.append({"fecha": fecha or date.today(), "usuario": usuario,
                                   "salario_base": empleado.salario_base, "cargo": empleado.cargo})
        if salario_base is not None:
            empleado.salario_base = salario_base
        if cargo is not None:
            empleado.cargo = cargo
        return self.repo.save(empleado)

    # ---------- D (lógico) ----------
    def desvincular(self, cedula):
        empleado = self.buscar(cedula)
        if empleado.estado == "INACTIVO":
            raise InvalidEmployeeException("El empleado ya está desvinculado")
        empleado.estado = "INACTIVO"
        self.repo.save(empleado)
        return MSG_DESVINCULADO

    def _validar_salario(self, salario):
        if salario < 0:
            raise InvalidEmployeeException("El salario no puede ser negativo")
        if salario < self.smmlv:
            raise InvalidEmployeeException("El salario no puede ser inferior al salario mínimo")
