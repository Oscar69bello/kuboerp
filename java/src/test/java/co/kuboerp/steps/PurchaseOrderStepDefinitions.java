package co.kuboerp.steps;

import co.kuboerp.dominio.PurchaseOrder;
import co.kuboerp.dominio.Supplier;
import io.cucumber.java.ParameterType;
import io.cucumber.java.es.Cuando;
import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Taller 3 · Aprobación de órdenes de compra. */
public class PurchaseOrderStepDefinitions {
    private static final String NIT_PROVEEDOR = "900123456";

    private final Contexto ctx;
    private String codigoOrden;

    public PurchaseOrderStepDefinitions(Contexto ctx) {
        this.ctx = ctx;
    }

    /** Convierte "$10.000.000" en 10000000. */
    @ParameterType("\\$[0-9.]+")
    public Long pesos(String valor) {
        return Long.parseLong(valor.replace("$", "").replace(".", ""));
    }

    @Dado("que el proveedor {string} tiene presupuesto disponible de {pesos}")
    public void queElProveedorTienePresupuesto(String nombre, Long presupuesto) {
        Supplier proveedor = ctx.supplierService.createSupplier(
                new Supplier(NIT_PROVEEDOR, nombre, "compras@electrocentro.com.co"));
        proveedor.setPresupuestoDisponible(presupuesto);
    }

    @Dado("que existe una orden {string} por {pesos} en estado {string}")
    public void queExisteUnaOrden(String codigo, Long monto, String estado) {
        ctx.ordenes.save(new PurchaseOrder(codigo, NIT_PROVEEDOR, monto, estado));
        codigoOrden = codigo;
    }

    @Cuando("el jefe de compras aprueba la orden")
    public void elJefeDeComprasApruebaLaOrden() {
        ctx.ejecutar(() -> {
            ctx.purchaseOrderService.approve(codigoOrden);
            return "Orden aprobada";
        });
    }

    @Entonces("la orden cambia a {string}")
    public void laOrdenCambiaA(String estado) {
        assertEquals(estado, ctx.ordenes.findByCodigo(codigoOrden).orElseThrow().getEstado());
    }

    @Entonces("la orden permanece en {string}")
    public void laOrdenPermaneceEn(String estado) {
        laOrdenCambiaA(estado);
    }

    @Entonces("el presupuesto del proveedor se reduce a {pesos}")
    public void elPresupuestoSeReduceA(Long esperado) {
        // Se consulta el presupuesto actualizado en el repositorio y se compara con el esperado.
        assertEquals(esperado, ctx.supplierService.findByNit(NIT_PROVEEDOR).getPresupuestoDisponible());
    }

    @Entonces("el presupuesto disponible del proveedor sigue en {pesos}")
    public void elPresupuestoSigueEn(Long esperado) {
        elPresupuestoSeReduceA(esperado);
    }
}
