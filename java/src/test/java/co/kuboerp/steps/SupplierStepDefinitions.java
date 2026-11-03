package co.kuboerp.steps;

import co.kuboerp.dominio.PurchaseOrder;
import co.kuboerp.dominio.Supplier;
import co.kuboerp.servicio.SupplierService;
import io.cucumber.java.es.Cuando;
import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;

import static org.junit.jupiter.api.Assertions.*;

/** Taller 1 y Ejercicio 1 · CRUD de proveedores. */
public class SupplierStepDefinitions {
    private final Contexto ctx;
    private Supplier proveedor;
    private String nitActual;
    private long proveedoresAntes;
    private boolean sesionIniciada;

    public SupplierStepDefinitions(Contexto ctx) {
        this.ctx = ctx;
    }

    @Dado("que el usuario administrador ha iniciado sesión")
    public void queElUsuarioAdministradorHaIniciadoSesion() {
        sesionIniciada = true;
        assertTrue(sesionIniciada);
    }

    @Dado("que no existe un proveedor con NIT {string}")
    public void queNoExisteProveedorConNit(String nit) {
        assertFalse(ctx.supplierService.existsByNit(nit));
    }

    @Cuando("registro el proveedor con NIT {string}, nombre {string} y correo {string}")
    public void registroProveedor(String nit, String nombre, String correo) {
        ctx.ejecutar(() -> {
            proveedor = ctx.supplierService.createSupplier(new Supplier(nit, nombre, correo));
            return SupplierService.MSG_REGISTRADO;
        });
    }

    @Entonces("el proveedor se crea con estado {string}")
    public void elProveedorSeCreaConEstado(String estado) {
        assertNotNull(proveedor);
        assertEquals(estado, proveedor.getEstado());
    }

    @Entonces("el sistema muestra el mensaje {string}")
    public void elSistemaMuestraMensaje(String mensaje) {
        assertEquals(mensaje, ctx.mensaje);
    }

    @Dado("que ya existe un proveedor con NIT {string}")
    public void queYaExisteProveedorConNit(String nit) {
        ctx.supplierService.createSupplier(
                new Supplier(nit, "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co"));
        nitActual = nit;
        proveedoresAntes = ctx.supplierService.count();
    }

    @Cuando("intento registrar otro proveedor con el mismo NIT")
    public void intentoRegistrarOtroProveedorConElMismoNit() {
        ctx.ejecutar(() -> {
            ctx.supplierService.createSupplier(
                    new Supplier(nitActual, "Schneider Electric Colombia", "ventas@schneider.com.co"));
            return SupplierService.MSG_REGISTRADO;
        });
    }

    @Entonces("no se crea un nuevo proveedor")
    public void noSeCreaUnNuevoProveedor() {
        assertEquals(proveedoresAntes, ctx.supplierService.count());
    }

    @Cuando("registro un proveedor con correo {string}")
    public void registroUnProveedorConCorreo(String correo) {
        ctx.ejecutar(() -> {
            ctx.supplierService.createSupplier(new Supplier("901555777", "Importadora LuzLED", correo));
            return "Correo válido";
        });
    }

    // ---- Ejercicio 1: eliminar (desactivar) proveedor ----

    @Dado("que existe un proveedor {string} con NIT {string} sin órdenes de compra activas")
    public void queExisteProveedorSinOrdenesActivas(String nombre, String nit) {
        ctx.supplierService.createSupplier(new Supplier(nit, nombre, "contacto@proveedor.com.co"));
        nitActual = nit;
        assertFalse(ctx.ordenes.hasActiveOrders(nit));
    }

    @Dado("que existe un proveedor {string} con NIT {string} y la orden de compra {string} en estado {string}")
    public void queExisteProveedorConOrden(String nombre, String nit, String orden, String estado) {
        ctx.supplierService.createSupplier(new Supplier(nit, nombre, "contacto@proveedor.com.co"));
        ctx.ordenes.save(new PurchaseOrder(orden, nit, 3_000_000, estado));
        nitActual = nit;
    }

    @Cuando("solicito eliminar el proveedor")
    public void solicitoEliminarElProveedor() {
        ctx.ejecutar(() -> ctx.supplierService.deleteSupplier(nitActual));
    }

    @Entonces("el proveedor cambia a estado {string}")
    public void elProveedorCambiaAEstado(String estado) {
        assertEquals(estado, ctx.supplierService.findByNit(nitActual).getEstado());
    }

    @Entonces("el proveedor sigue en estado {string}")
    public void elProveedorSigueEnEstado(String estado) {
        assertEquals(estado, ctx.supplierService.findByNit(nitActual).getEstado());
    }
}
