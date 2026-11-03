"""Taller 1 · CRUD de proveedores de material eléctrico."""
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

    def count(self):
        return len(self._datos)


class InMemoryOrderRepository:
    """Repositorio mínimo de órdenes: solo responde si un proveedor tiene órdenes activas."""

    def __init__(self, nits_con_ordenes=()):
        self._nits = set(nits_con_ordenes)

    def has_active_orders(self, nit):
        return nit in self._nits


class SupplierService:
    def __init__(self, repo=None, repo_ordenes=None):
        self.repo = repo if repo is not None else InMemorySupplierRepository()
        self.repo_ordenes = repo_ordenes if repo_ordenes is not None else InMemoryOrderRepository()

    @staticmethod
    def es_nit_valido(nit):
        return bool(nit) and bool(_NIT.match(nit))

    @staticmethod
    def es_correo_valido(correo):
        return bool(correo) and bool(_CORREO.match(correo))

    def existe_por_nit(self, nit):
        return self.repo.find_by_nit(nit) is not None

    def create_supplier(self, nit, nombre, correo):
        if not self.es_nit_valido(nit):
            raise InvalidSupplierException("NIT inválido")
        if not nombre or not nombre.strip():
            raise InvalidSupplierException("El nombre es obligatorio")
        if not self.es_correo_valido(correo):
            raise InvalidSupplierException("Formato de correo inválido")
        if self.existe_por_nit(nit):
            raise InvalidSupplierException("El NIT ya está registrado")
        return self.repo.save(Supplier(nit, nombre.strip(), correo))

    def buscar(self, nit):
        proveedor = self.repo.find_by_nit(nit)
        if proveedor is None:
            raise InvalidSupplierException("Proveedor no encontrado")
        return proveedor

    def delete_supplier(self, nit):
        """Eliminación lógica: el proveedor pasa a INACTIVO si no tiene órdenes activas."""
        if self.repo_ordenes.has_active_orders(nit):
            raise SupplierHasActiveOrdersException(
                "No se puede eliminar un proveedor con órdenes de compra activas")
        proveedor = self.buscar(nit)
        proveedor.estado = "INACTIVO"
        self.repo.save(proveedor)
        return MSG_DESACTIVADO
