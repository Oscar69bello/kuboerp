"""Taller 3 · Aprobación de órdenes de compra (pytest con fixtures)."""
import pytest

from kuboerp.excepciones import PurchaseOrderException
from kuboerp.ordenes import InMemoryPurchaseOrderRepository, PurchaseOrder, PurchaseOrderService
from kuboerp.proveedores import InMemorySupplierRepository, Supplier

NIT = "900123456"


@pytest.fixture
def repos():
    proveedores = InMemorySupplierRepository()
    proveedores.save(Supplier(NIT, "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co",
                              presupuesto=10_000_000))
    return proveedores, InMemoryPurchaseOrderRepository()


def test_aprobar_orden_dentro_del_presupuesto(repos):
    proveedores, ordenes = repos
    ordenes.save(PurchaseOrder("OC-0001", NIT, 5_000_000))

    orden = PurchaseOrderService(proveedores, ordenes).approve("OC-0001")

    assert orden.estado == "APROBADA"
    assert proveedores.find_by_nit(NIT).presupuesto == 5_000_000


def test_rechazar_orden_que_excede_el_presupuesto(repos):
    proveedores, ordenes = repos
    ordenes.save(PurchaseOrder("OC-0002", NIT, 15_000_000))

    with pytest.raises(PurchaseOrderException, match="Presupuesto insuficiente"):
        PurchaseOrderService(proveedores, ordenes).approve("OC-0002")
    assert ordenes.find_by_codigo("OC-0002").estado == "PENDIENTE"
    assert proveedores.find_by_nit(NIT).presupuesto == 10_000_000


def test_no_volver_a_aprobar_una_orden_aprobada(repos):
    proveedores, ordenes = repos
    ordenes.save(PurchaseOrder("OC-0003", NIT, 1_000_000, "APROBADA"))

    with pytest.raises(PurchaseOrderException, match="La orden ya está aprobada"):
        PurchaseOrderService(proveedores, ordenes).approve("OC-0003")
