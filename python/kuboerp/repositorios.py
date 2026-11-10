"""Sprint 2 · Contratos (puertos) que usan los servicios de KuboERP.

Principios SOLID aplicados:
* D (Inversión de dependencias): los servicios dependen de estos protocolos y no de una base de datos
  concreta. Hoy se inyectan repositorios en memoria; en producción se inyectará el adaptador de Azure SQL
  sin cambiar los servicios.
* I (Segregación de interfaces): cada servicio pide solo los métodos que usa. Por ejemplo, el servicio de
  proveedores solo necesita saber si un proveedor tiene órdenes activas (VerificadorOrdenesActivas), no todo
  el repositorio de órdenes.
"""
from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class RepositorioProveedores(Protocol):
    def save(self, proveedor): ...

    def find_by_nit(self, nit: str): ...

    def find_all(self) -> list: ...


@runtime_checkable
class RepositorioCotizaciones(Protocol):
    def add_request(self, codigo: str, estado: str = "ABIERTA"): ...

    def find_request(self, codigo: str): ...

    def exists_by_request_and_supplier(self, solicitud: str, nit: str) -> bool: ...

    def find_by_codigo(self, codigo: str): ...

    def find_by_request(self, solicitud: str) -> list: ...

    def save(self, cotizacion): ...


@runtime_checkable
class VerificadorOrdenesActivas(Protocol):
    def has_active_orders(self, nit: str) -> bool: ...


@runtime_checkable
class RepositorioOrdenes(VerificadorOrdenesActivas, Protocol):
    def save(self, orden): ...

    def find_by_codigo(self, codigo: str): ...

    def find_all(self) -> list: ...


@runtime_checkable
class RepositorioProductos(Protocol):
    movimientos: list

    def save(self, producto): ...

    def find_by_code(self, codigo: str): ...

    def find_all(self) -> list: ...


@runtime_checkable
class EntradaInventario(Protocol):
    """Lo único que el módulo de compras necesita del inventario: registrar una entrada."""

    def update_stock(self, product_id: str, quantity: int) -> int: ...


@runtime_checkable
class ObservadorStock(Protocol):
    """Recibe un aviso cuando un producto queda en stock crítico (patrón Observer)."""

    def notificar(self, alerta) -> None: ...


@runtime_checkable
class RepositorioEmpleados(Protocol):
    def save(self, empleado): ...

    def find_by_cedula(self, cedula: str) -> Optional[object]: ...

    def find_all(self) -> list: ...
