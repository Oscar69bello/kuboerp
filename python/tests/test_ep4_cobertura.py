"""Ejercicio práctico 4 · Pruebas agregadas para cubrir las líneas que coverage reportó sin probar.

Antes de este archivo la cobertura era 92 %. Líneas faltantes:
  cotizaciones.py 20-21, 24, 27, 30, 33-34 · repositorio en memoria (las pruebas usaban MagicMock)
  inventario.py   41, 70                    · código vacío y producto inexistente
  ordenes.py      27, 39                    · órdenes activas en el repositorio y orden inexistente
  proveedores.py  35, 45, 68, 72, 78        · conteo, repositorio de órdenes, nombre vacío,
                                              NIT duplicado y proveedor inexistente
Hallazgo: la regla "NIT único" (línea 72) solo la probaba el escenario BDD de Behave;
ninguna prueba unitaria la cubría. Con este archivo la cobertura sube a 100 %.
"""
import pytest

from kuboerp.cotizaciones import InMemoryQuotationRepository, QuotationService
from kuboerp.excepciones import (InvalidProductException, InvalidQuotationException,
                                 InvalidSupplierException, PurchaseOrderException)
from kuboerp.inventario import InventoryService
from kuboerp.ordenes import InMemoryPurchaseOrderRepository, PurchaseOrder, PurchaseOrderService
from kuboerp.proveedores import InMemorySupplierRepository, SupplierService


def test_cotizaciones_con_repositorio_en_memoria():
    repo = InMemoryQuotationRepository()
    repo.add_request("SC-0001")
    service = QuotationService(repo)

    cotizacion = service.registrar("COT-0001", "SC-0001", "901555777", 2300000)

    assert cotizacion.estado == "RECIBIDA"
    with pytest.raises(InvalidQuotationException, match="El proveedor ya cotizó esta solicitud"):
        service.registrar("COT-0002", "SC-0001", "901555777", 2100000)
    with pytest.raises(InvalidQuotationException, match="La solicitud no está abierta"):
        service.registrar("COT-0003", "SC-9999", "901555777", 2100000)


def test_inventario_rechaza_codigo_vacio_y_producto_inexistente():
    service = InventoryService()
    with pytest.raises(InvalidProductException, match="El código es obligatorio"):
        service.register_product("", "Pinza voltiamperimétrica", "Herramientas", 8)
    with pytest.raises(InvalidProductException, match="Producto no encontrado"):
        service.stock_de("PINZA-VA-01")


def test_ordenes_inexistentes_y_ordenes_activas_por_proveedor():
    ordenes = InMemoryPurchaseOrderRepository()
    ordenes.save(PurchaseOrder("OC-0001", "900888111", 3_000_000))
    service = PurchaseOrderService(InMemorySupplierRepository(), ordenes)

    assert ordenes.has_active_orders("900888111")
    assert not ordenes.has_active_orders("901555777")
    with pytest.raises(PurchaseOrderException, match="Orden no encontrada"):
        service.approve("OC-9999")


def test_proveedores_nombre_vacio_inexistente_y_conteo():
    service = SupplierService()
    with pytest.raises(InvalidSupplierException, match="El nombre es obligatorio"):
        service.create_supplier("900123456", "   ", "compras@electrocentro.com.co")
    with pytest.raises(InvalidSupplierException, match="Proveedor no encontrado"):
        service.delete_supplier("999999999")

    service.create_supplier("900123456", "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co")
    assert service.repo.count() == 1


def test_proveedor_con_nit_duplicado_no_se_crea():
    service = SupplierService()
    service.create_supplier("900123456", "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co")

    with pytest.raises(InvalidSupplierException, match="El NIT ya está registrado"):
        service.create_supplier("900123456", "Schneider Electric Colombia", "ventas@schneider.com.co")
    assert service.repo.count() == 1
