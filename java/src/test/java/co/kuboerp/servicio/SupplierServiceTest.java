package co.kuboerp.servicio;

import co.kuboerp.dominio.InvalidSupplierException;
import co.kuboerp.dominio.Supplier;
import co.kuboerp.dominio.SupplierHasActiveOrdersException;
import co.kuboerp.repositorio.InMemorySupplierRepository;
import co.kuboerp.repositorio.PurchaseOrderRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("KuboERP · Pruebas del servicio de proveedores")
class SupplierServiceTest {

    private SupplierService service;

    @BeforeEach
    void setUp() {
        service = new SupplierService(new InMemorySupplierRepository());
    }

    @Test
    @DisplayName("Debe crear un proveedor con NIT válido")
    void deberiaCrearProveedorConNitValido() {
        Supplier proveedor = new Supplier("900123456", "Distribuidora Eléctrica del Centro S.A.S.",
                "compras@electrocentro.com.co");

        Supplier creado = service.createSupplier(proveedor);

        assertNotNull(creado.getId());
        assertEquals("ACTIVO", creado.getEstado());
    }

    @Test
    @DisplayName("Debe rechazar NIT duplicado")
    void noDeberiaCrearProveedorConNitDuplicado() {
        service.createSupplier(new Supplier("900123456", "Distribuidora Eléctrica del Centro", "a@centro.com"));
        Supplier duplicado = new Supplier("900123456", "Schneider Electric Colombia", "b@schneider.com.co");

        InvalidSupplierException error =
                assertThrows(InvalidSupplierException.class, () -> service.createSupplier(duplicado));
        assertEquals("El NIT ya está registrado", error.getMessage());
        assertEquals(1, service.count());
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "sin-arroba", "usuario@"})
    @DisplayName("Debe rechazar correos inválidos")
    void noDeberiaAceptarCorreosInvalidos(String correo) {
        Supplier proveedor = new Supplier("900999999", "Importadora LuzLED", correo);

        assertThrows(InvalidSupplierException.class, () -> service.createSupplier(proveedor));
    }

    @Test
    @DisplayName("Taller 1 · No debe eliminar un proveedor con órdenes de compra activas")
    void noDeberiaEliminarProveedorConOrdenesActivas() {
        PurchaseOrderRepository ordenes = mock(PurchaseOrderRepository.class);
        when(ordenes.hasActiveOrders("900888111")).thenReturn(true);
        SupplierService servicio = new SupplierService(new InMemorySupplierRepository(), ordenes);
        servicio.createSupplier(new Supplier("900888111", "Procables S.A.S.",
                "ventas@procables.com.co"));

        assertThrows(SupplierHasActiveOrdersException.class, () -> servicio.deleteSupplier("900888111"));

        assertEquals("ACTIVO", servicio.findByNit("900888111").getEstado());
        verify(ordenes).hasActiveOrders("900888111");
    }

    @Test
    @DisplayName("Taller 1 · Debe desactivar un proveedor sin órdenes de compra activas")
    void deberiaDesactivarProveedorSinOrdenesActivas() {
        PurchaseOrderRepository ordenes = mock(PurchaseOrderRepository.class);
        when(ordenes.hasActiveOrders("901555777")).thenReturn(false);
        SupplierService servicio = new SupplierService(new InMemorySupplierRepository(), ordenes);
        servicio.createSupplier(new Supplier("901555777", "Importadora LuzLED S.A.S.", "ventas@luzled.co"));

        String mensaje = servicio.deleteSupplier("901555777");

        assertEquals("Proveedor desactivado", mensaje);
        assertEquals("INACTIVO", servicio.findByNit("901555777").getEstado());
    }
}
