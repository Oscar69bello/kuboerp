"""Sprint 2 · CRUD de proveedores, cotizaciones y órdenes de compra (pytest).

Cada prueba sigue el patrón Arrange · Act · Assert y usa repositorios en memoria (inyección de
dependencias), así que no necesita base de datos.
"""
import pytest

from kuboerp.cotizaciones import QuotationService
from kuboerp.excepciones import (InvalidQuotationException, InvalidSupplierException,
                                 PurchaseOrderException, SupplierHasActiveOrdersException)
from kuboerp.inventario import InventoryService
from kuboerp.ordenes import InMemoryPurchaseOrderRepository, LineaOrden, PurchaseOrderService
from kuboerp.proveedores import InMemorySupplierRepository, SupplierService

NIT = "900123456"
NIT_2 = "901555777"


@pytest.fixture
def compras():
    """Proveedores, órdenes e inventario conectados como en producción, pero en memoria."""
    repo_proveedores = InMemorySupplierRepository()
    repo_ordenes = InMemoryPurchaseOrderRepository()
    proveedores = SupplierService(repo_proveedores, repo_ordenes)
    inventario = InventoryService()
    ordenes = PurchaseOrderService(repo_proveedores, repo_ordenes, inventario)

    proveedores.create_supplier(NIT, "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co",
                                presupuesto=10_000_000)
    inventario.register_product("CAB-THHN-12", "Cable THHN 12 AWG (rollo 100 m)", "Cables", 5, 10)
    inventario.register_product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 40, 15)
    return proveedores, ordenes, inventario


LINEAS = [LineaOrden("CAB-THHN-12", 20, 180_000), LineaOrden("BRK-2X30", 10, 45_000)]


# ---------------------------------------------------------------- proveedores
class TestProveedoresCrud:
    def test_listar_ordena_por_nombre_y_filtra_por_estado(self, compras):
        proveedores, _, _ = compras
        proveedores.create_supplier(NIT_2, "Andina de Iluminación", "ventas@andinaluz.com")
        proveedores.delete_supplier(NIT_2)

        assert [p.nit for p in proveedores.listar()] == [NIT_2, NIT]
        assert [p.nit for p in proveedores.listar("ACTIVO")] == [NIT]
        assert [p.nit for p in proveedores.listar("INACTIVO")] == [NIT_2]

    def test_actualizar_nombre_correo_y_presupuesto(self, compras):
        proveedores, _, _ = compras

        actualizado = proveedores.update_supplier(NIT, nombre="  Electrocentro S.A.S. ",
                                                  correo="pedidos@electrocentro.com.co",
                                                  presupuesto=12_000_000)

        assert actualizado.nombre == "Electrocentro S.A.S."
        assert actualizado.correo == "pedidos@electrocentro.com.co"
        assert proveedores.buscar(NIT).presupuesto == 12_000_000

    @pytest.mark.parametrize("cambios, mensaje", [
        ({"nombre": " "}, "El nombre es obligatorio"),
        ({"correo": "pedidos-electrocentro"}, "Formato de correo inválido"),
        ({"presupuesto": -1}, "El presupuesto no puede ser negativo"),
    ])
    def test_actualizar_con_datos_invalidos_no_cambia_el_proveedor(self, compras, cambios, mensaje):
        proveedores, _, _ = compras
        with pytest.raises(InvalidSupplierException, match=mensaje):
            proveedores.update_supplier(NIT, **cambios)
        assert proveedores.buscar(NIT).nombre == "Distribuidora Eléctrica del Centro"

    def test_no_crear_con_presupuesto_negativo(self, compras):
        proveedores, _, _ = compras
        with pytest.raises(InvalidSupplierException, match="El presupuesto no puede ser negativo"):
            proveedores.create_supplier(NIT_2, "Andina de Iluminación", "ventas@andinaluz.com", -5)

    def test_esta_activo(self, compras):
        proveedores, _, _ = compras
        assert proveedores.esta_activo(NIT)
        assert not proveedores.esta_activo("999999999")

    def test_no_desactivar_proveedor_con_orden_pendiente_del_repositorio_real(self, compras):
        proveedores, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        with pytest.raises(SupplierHasActiveOrdersException):
            proveedores.delete_supplier(NIT)


# ---------------------------------------------------------------- cotizaciones
class TestCotizacionesCrud:
    @pytest.fixture
    def servicio(self):
        servicio = QuotationService()
        servicio.abrir_solicitud("SC-0001")
        servicio.registrar("COT-0001", "SC-0001", NIT, 2_300_000)
        servicio.registrar("COT-0002", "SC-0001", NIT_2, 2_100_000)
        return servicio

    def test_abrir_solicitud_valida_codigo_y_duplicado(self, servicio):
        with pytest.raises(InvalidQuotationException, match="obligatorio"):
            servicio.abrir_solicitud("")
        with pytest.raises(InvalidQuotationException, match="La solicitud ya existe"):
            servicio.abrir_solicitud("SC-0001")

    def test_codigo_de_cotizacion_unico(self, servicio):
        with pytest.raises(InvalidQuotationException, match="El código de la cotización ya existe"):
            servicio.registrar("COT-0001", "SC-0001", "830000111", 1_900_000)

    def test_listar_por_solicitud_de_la_mas_barata_a_la_mas_cara(self, servicio):
        assert [c.codigo for c in servicio.listar_por_solicitud("SC-0001")] == ["COT-0002", "COT-0001"]

    def test_actualizar_monto(self, servicio):
        assert servicio.actualizar_monto("COT-0001", 2_000_000).monto == 2_000_000
        with pytest.raises(InvalidQuotationException, match="Monto inválido"):
            servicio.actualizar_monto("COT-0001", 0)

    def test_seleccionar_rechaza_las_demas_y_cierra_la_solicitud(self, servicio):
        ganadora = servicio.seleccionar("COT-0002")

        assert ganadora.estado == "SELECCIONADA"
        assert servicio.buscar("COT-0001").estado == "RECHAZADA"
        with pytest.raises(InvalidQuotationException, match="La solicitud no está abierta"):
            servicio.registrar("COT-0003", "SC-0001", "830000111", 1_000_000)

    def test_anular_permite_que_el_proveedor_vuelva_a_cotizar(self, servicio):
        assert servicio.anular("COT-0001") == "Cotización anulada"
        assert [c.codigo for c in servicio.listar_por_solicitud("SC-0001")] == ["COT-0002"]

        nueva = servicio.registrar("COT-0003", "SC-0001", NIT, 1_950_000)
        assert nueva.estado == "RECIBIDA"

    def test_no_modificar_cotizacion_que_no_esta_recibida(self, servicio):
        servicio.anular("COT-0001")
        with pytest.raises(InvalidQuotationException, match="Solo se modifican cotizaciones"):
            servicio.actualizar_monto("COT-0001", 1_000_000)

    def test_cotizacion_inexistente(self, servicio):
        with pytest.raises(InvalidQuotationException, match="Cotización no encontrada"):
            servicio.buscar("COT-9999")


# ---------------------------------------------------------------- órdenes de compra
class TestOrdenesCrud:
    def test_crear_calcula_el_monto_con_las_lineas(self, compras):
        _, ordenes, _ = compras

        orden = ordenes.crear("OC-0001", NIT, LINEAS)

        assert orden.estado == "PENDIENTE"
        assert orden.monto == 20 * 180_000 + 10 * 45_000      # 4.050.000
        assert ordenes.auditoria[-1] == ("OC-0001", "", "PENDIENTE", "Orden creada")

    @pytest.mark.parametrize("codigo, nit, lineas, mensaje", [
        ("", NIT, LINEAS, "El código de la orden es obligatorio"),
        ("OC-0002", "999999999", LINEAS, "El proveedor no existe o está inactivo"),
        ("OC-0002", NIT, [], "al menos un producto"),
        ("OC-0002", NIT, [LineaOrden("BRK-2X30", 0, 45_000)], "mayores que cero"),
        ("OC-0002", NIT, [LineaOrden("BRK-2X30", 3, -1)], "mayores que cero"),
    ])
    def test_crear_con_datos_invalidos(self, compras, codigo, nit, lineas, mensaje):
        _, ordenes, _ = compras
        with pytest.raises(PurchaseOrderException, match=mensaje):
            ordenes.crear(codigo, nit, lineas)

    def test_no_crear_orden_a_proveedor_inactivo_ni_con_codigo_repetido(self, compras):
        proveedores, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        with pytest.raises(PurchaseOrderException, match="El código de la orden ya existe"):
            ordenes.crear("OC-0001", NIT, LINEAS)

        proveedores.create_supplier(NIT_2, "Andina de Iluminación", "ventas@andinaluz.com")
        proveedores.delete_supplier(NIT_2)
        with pytest.raises(PurchaseOrderException, match="inactivo"):
            ordenes.crear("OC-0002", NIT_2, LINEAS)

    def test_listar_por_estado_y_proveedor(self, compras):
        _, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        ordenes.crear("OC-0002", NIT, LINEAS)
        ordenes.approve("OC-0002")

        assert [o.codigo for o in ordenes.listar("PENDIENTE")] == ["OC-0001"]
        assert len(ordenes.listar(nit_proveedor=NIT)) == 2
        assert ordenes.listar(nit_proveedor=NIT_2) == []

    def test_recibir_genera_entrada_de_inventario(self, compras):
        _, ordenes, inventario = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        ordenes.approve("OC-0001")

        orden = ordenes.recibir("OC-0001")

        assert orden.estado == "RECIBIDA"
        assert inventario.stock_de("CAB-THHN-12") == 25
        assert inventario.stock_de("BRK-2X30") == 50
        assert [a[2] for a in ordenes.auditoria] == ["PENDIENTE", "APROBADA", "RECIBIDA"]

    def test_recibir_sin_inventario_conectado_solo_cambia_el_estado(self, compras):
        proveedores, _, _ = compras
        ordenes = PurchaseOrderService(proveedores.repo, InMemoryPurchaseOrderRepository())
        ordenes.crear("OC-0001", NIT, LINEAS)
        ordenes.approve("OC-0001")
        assert ordenes.recibir("OC-0001").estado == "RECIBIDA"

    def test_no_recibir_orden_pendiente(self, compras):
        _, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        with pytest.raises(PurchaseOrderException, match="Solo se reciben órdenes aprobadas"):
            ordenes.recibir("OC-0001")

    def test_cancelar_orden_aprobada_devuelve_el_presupuesto(self, compras):
        proveedores, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        ordenes.approve("OC-0001")
        assert proveedores.buscar(NIT).presupuesto == 5_950_000

        orden = ordenes.cancelar("OC-0001", "  El proveedor no tiene el cable en bodega ")

        assert orden.estado == "CANCELADA"
        assert orden.justificacion == "El proveedor no tiene el cable en bodega"
        assert proveedores.buscar(NIT).presupuesto == 10_000_000

    def test_cancelar_exige_justificacion_y_estado_activo(self, compras):
        _, ordenes, _ = compras
        ordenes.crear("OC-0001", NIT, LINEAS)
        with pytest.raises(PurchaseOrderException, match="exige una justificación"):
            ordenes.cancelar("OC-0001", "  ")

        ordenes.cancelar("OC-0001", "Compra duplicada")
        with pytest.raises(PurchaseOrderException, match="Solo se cancelan"):
            ordenes.cancelar("OC-0001", "Otra vez")
        with pytest.raises(PurchaseOrderException, match="Solo se aprueban órdenes pendientes"):
            ordenes.approve("OC-0001")
