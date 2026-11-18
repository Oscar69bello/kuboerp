"""CRUD de proveedores de material eléctrico (EP05-US01, EP05-US02, EP05-US04).

Taller 1 (Sprint 2 · TDD) creó el registro y la desactivación. El taller de Sprint Planning y CRUD en
Python completa la consulta (listar) y la actualización.
"""
import re
from dataclasses import dataclass

from kuboerp.excepciones import InvalidSupplierException, SupplierHasActiveOrdersException

MSG_REGISTRADO = "Proveedor registrado exitosamente"
MSG_DESACTIVADO = "Proveedor desactivado"

_NIT = re.compile(r"^\d{9,10}$")
_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


@dataclass
class Supplier:
    nit: str
    nombre: str
    correo: str
    estado: str = "ACTIVO"
    presupuesto: int = 0


class InMemorySupplierRepository:
    def __init__(self):
        self._datos = {}

    def save(self, proveedor):
        self._datos[proveedor.nit] = proveedor
        return proveedor

    def find_by_nit(self, nit):
        return self._datos.get(nit)

    def find_all(self):
        return list(self._datos.values())

    def count(self):
        return len(self._datos)


class InMemoryOrderRepository:
    """Repositorio mínimo de órdenes: solo responde si un proveedor tiene órdenes activas."""

    def __init__(self, nits_con_ordenes=()):
        self._nits = set(nits_con_ordenes)

    def has_active_orders(self, nit):
        return nit in self._nits


class SupplierService:
    """Responsabilidad única: reglas de negocio de los proveedores.

    No sabe cómo se guardan los datos (recibe el repositorio por constructor) ni cómo se gestionan las
    órdenes (solo pregunta has_active_orders).
    """

    def __init__(self, repo=None, repo_ordenes=None):
        self.repo = repo if repo is not None else InMemorySupplierRepository()
        self.repo_ordenes = repo_ordenes if repo_ordenes is not None else InMemoryOrderRepository()

    # ---------- validaciones ----------
    @staticmethod
    def es_nit_valido(nit):
        return bool(nit) and bool(_NIT.match(nit))

    @staticmethod
    def es_correo_valido(correo):
        return bool(correo) and bool(_CORREO.match(correo))

    def existe_por_nit(self, nit):
        return self.repo.find_by_nit(nit) is not None

    @staticmethod
    def _validar_nombre(nombre):
        if not nombre or not nombre.strip():
            raise InvalidSupplierException("El nombre es obligatorio")

    def _validar_correo(self, correo):
        if not self.es_correo_valido(correo):
            raise InvalidSupplierException("Formato de correo inválido")

    # ---------- C ----------
    def create_supplier(self, nit, nombre, correo, presupuesto=0):
        if not self.es_nit_valido(nit):
            raise InvalidSupplierException("NIT inválido")
        self._validar_nombre(nombre)
        self._validar_correo(correo)
        if presupuesto < 0:
            raise InvalidSupplierException("El presupuesto no puede ser negativo")
        if self.existe_por_nit(nit):
            raise InvalidSupplierException("El NIT ya está registrado")
        return self.repo.save(Supplier(nit, nombre.strip(), correo, presupuesto=presupuesto))

    # ---------- R ----------
    def buscar(self, nit):
        proveedor = self.repo.find_by_nit(nit)
        if proveedor is None:
            raise InvalidSupplierException("Proveedor no encontrado")
        return proveedor

    def listar(self, estado=None):
        """Lista los proveedores ordenados por nombre; con estado filtra ACTIVO o INACTIVO."""
        proveedores = [p for p in self.repo.find_all() if estado is None or p.estado == estado]
        return sorted(proveedores, key=lambda p: p.nombre)

    def esta_activo(self, nit):
        proveedor = self.repo.find_by_nit(nit)
        return proveedor is not None and proveedor.estado == "ACTIVO"

    # ---------- U ----------
    def update_supplier(self, nit, nombre=None, correo=None, presupuesto=None):
        """Actualiza los datos editables. El NIT es la identidad del proveedor y no se cambia."""
        proveedor = self.buscar(nit)
        if nombre is not None:
            self._validar_nombre(nombre)
            proveedor.nombre = nombre.strip()
        if correo is not None:
            self._validar_correo(correo)
            proveedor.correo = correo
        if presupuesto is not None:
            if presupuesto < 0:
                raise InvalidSupplierException("El presupuesto no puede ser negativo")
            proveedor.presupuesto = presupuesto
        return self.repo.save(proveedor)

    # ---------- D (lógico) ----------
    def delete_supplier(self, nit):
        """Eliminación lógica: el proveedor pasa a INACTIVO si no tiene órdenes activas."""
        if self.repo_ordenes.has_active_orders(nit):
            raise SupplierHasActiveOrdersException(
                "No se puede eliminar un proveedor con órdenes de compra activas")
        proveedor = self.buscar(nit)
        proveedor.estado = "INACTIVO"
        self.repo.save(proveedor)
        return MSG_DESACTIVADO
