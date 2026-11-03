"""Taller 3 · Aprobación de órdenes de compra contra el presupuesto del proveedor."""
from dataclasses import dataclass

from kuboerp.excepciones import PurchaseOrderException


@dataclass
class PurchaseOrder:
    codigo: str
    nit_proveedor: str
    monto: int
    estado: str = "PENDIENTE"


class InMemoryPurchaseOrderRepository:
    def __init__(self):
        self._datos = {}

    def save(self, orden):
        self._datos[orden.codigo] = orden
        return orden

    def find_by_codigo(self, codigo):
        return self._datos.get(codigo)

    def has_active_orders(self, nit):
        return any(o.nit_proveedor == nit and o.estado in ("PENDIENTE", "APROBADA")
                   for o in self._datos.values())


class PurchaseOrderService:
    def __init__(self, repo_proveedores, repo_ordenes):
        self.repo_proveedores = repo_proveedores
        self.repo_ordenes = repo_ordenes

    def approve(self, codigo):
        orden = self.repo_ordenes.find_by_codigo(codigo)
        if orden is None:
            raise PurchaseOrderException("Orden no encontrada")
        if orden.estado == "APROBADA":
            raise PurchaseOrderException("La orden ya está aprobada")
        proveedor = self.repo_proveedores.find_by_nit(orden.nit_proveedor)
        if orden.monto > proveedor.presupuesto:
            raise PurchaseOrderException("Presupuesto insuficiente")
        proveedor.presupuesto -= orden.monto
        self.repo_proveedores.save(proveedor)
        orden.estado = "APROBADA"
        return self.repo_ordenes.save(orden)
