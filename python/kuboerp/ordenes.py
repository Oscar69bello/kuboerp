"""CRUD de órdenes de compra (EP05-US05, EP05-US06).

Ciclo de vida:  PENDIENTE → APROBADA → RECIBIDA
                PENDIENTE | APROBADA → CANCELADA (con justificación)

* Aprobar descuenta el monto del presupuesto del proveedor (Taller 3).
* Recibir genera la entrada de cada producto en el inventario.
* Cancelar una orden aprobada devuelve el monto al presupuesto.
* Cada cambio de estado queda en el log de auditoría.
"""
from dataclasses import dataclass, field

from kuboerp.excepciones import PurchaseOrderException

ESTADOS_ACTIVOS = ("PENDIENTE", "APROBADA")


@dataclass
class LineaOrden:
    codigo_producto: str
    cantidad: int
    precio_unitario: int

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


@dataclass
class PurchaseOrder:
    codigo: str
    nit_proveedor: str
    monto: int
    estado: str = "PENDIENTE"
    lineas: list = field(default_factory=list)
    justificacion: str = ""


class InMemoryPurchaseOrderRepository:
    def __init__(self):
        self._datos = {}

    def save(self, orden):
        self._datos[orden.codigo] = orden
        return orden

    def find_by_codigo(self, codigo):
        return self._datos.get(codigo)

    def find_all(self):
        return list(self._datos.values())

    def has_active_orders(self, nit):
        return any(o.nit_proveedor == nit and o.estado in ESTADOS_ACTIVOS
                   for o in self._datos.values())


class PurchaseOrderService:
    """Depende de abstracciones: repositorios y un puerto de EntradaInventario (SOLID · D)."""

    def __init__(self, repo_proveedores, repo_ordenes, inventario=None):
        self.repo_proveedores = repo_proveedores
        self.repo_ordenes = repo_ordenes
        self.inventario = inventario
        self.auditoria = []        # (orden, estado anterior, estado nuevo, detalle)

    # ---------- C ----------
    def crear(self, codigo, nit_proveedor, lineas):
        if not codigo:
            raise PurchaseOrderException("El código de la orden es obligatorio")
        if self.repo_ordenes.find_by_codigo(codigo) is not None:
            raise PurchaseOrderException("El código de la orden ya existe")
        proveedor = self.repo_proveedores.find_by_nit(nit_proveedor)
        if proveedor is None or proveedor.estado != "ACTIVO":
            raise PurchaseOrderException("El proveedor no existe o está inactivo")
        if not lineas:
            raise PurchaseOrderException("La orden debe tener al menos un producto")
        if any(linea.cantidad <= 0 or linea.precio_unitario <= 0 for linea in lineas):
            raise PurchaseOrderException("Cantidad y precio unitario deben ser mayores que cero")
        monto = sum(linea.subtotal for linea in lineas)
        orden = PurchaseOrder(codigo, nit_proveedor, monto, lineas=list(lineas))
        self._auditar(orden, "", "PENDIENTE", "Orden creada")
        return self.repo_ordenes.save(orden)

    # ---------- R ----------
    def buscar(self, codigo):
        orden = self.repo_ordenes.find_by_codigo(codigo)
        if orden is None:
            raise PurchaseOrderException("Orden no encontrada")
        return orden

    def listar(self, estado=None, nit_proveedor=None):
        return [o for o in self.repo_ordenes.find_all()
                if (estado is None or o.estado == estado)
                and (nit_proveedor is None or o.nit_proveedor == nit_proveedor)]

    # ---------- U ----------
    def approve(self, codigo):
        orden = self.buscar(codigo)
        if orden.estado == "APROBADA":
            raise PurchaseOrderException("La orden ya está aprobada")
        if orden.estado != "PENDIENTE":
            raise PurchaseOrderException("Solo se aprueban órdenes pendientes")
        proveedor = self.repo_proveedores.find_by_nit(orden.nit_proveedor)
        if orden.monto > proveedor.presupuesto:
            raise PurchaseOrderException("Presupuesto insuficiente")
        proveedor.presupuesto -= orden.monto
        self.repo_proveedores.save(proveedor)
        return self._cambiar_estado(orden, "APROBADA", "Presupuesto descontado")

    def recibir(self, codigo):
        orden = self.buscar(codigo)
        if orden.estado != "APROBADA":
            raise PurchaseOrderException("Solo se reciben órdenes aprobadas")
        if self.inventario is not None:
            for linea in orden.lineas:
                self.inventario.update_stock(linea.codigo_producto, linea.cantidad)
        return self._cambiar_estado(orden, "RECIBIDA", "Entrada de inventario generada")

    # ---------- D (lógico) ----------
    def cancelar(self, codigo, justificacion):
        orden = self.buscar(codigo)
        if orden.estado not in ESTADOS_ACTIVOS:
            raise PurchaseOrderException("Solo se cancelan órdenes pendientes o aprobadas")
        if not justificacion or not justificacion.strip():
            raise PurchaseOrderException("La cancelación exige una justificación")
        if orden.estado == "APROBADA":
            proveedor = self.repo_proveedores.find_by_nit(orden.nit_proveedor)
            proveedor.presupuesto += orden.monto
            self.repo_proveedores.save(proveedor)
        orden.justificacion = justificacion.strip()
        return self._cambiar_estado(orden, "CANCELADA", orden.justificacion)

    def _cambiar_estado(self, orden, nuevo, detalle):
        self._auditar(orden, orden.estado, nuevo, detalle)
        orden.estado = nuevo
        return self.repo_ordenes.save(orden)

    def _auditar(self, orden, anterior, nuevo, detalle):
        self.auditoria.append((orden.codigo, anterior, nuevo, detalle))
