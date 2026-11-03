package co.kuboerp.steps;

import co.kuboerp.repositorio.InMemoryProductRepository;
import co.kuboerp.repositorio.InMemoryPurchaseOrderRepository;
import co.kuboerp.repositorio.InMemorySupplierRepository;
import co.kuboerp.servicio.InventoryService;
import co.kuboerp.servicio.PurchaseOrderService;
import co.kuboerp.servicio.QuotationService;
import co.kuboerp.servicio.SupplierService;
import java.util.function.Supplier;

/**
 * Estado compartido por los step definitions de un escenario.
 * PicoContainer crea una instancia nueva por escenario y la inyecta en cada clase de pasos.
 */
public class Contexto {
    public final InMemorySupplierRepository proveedores = new InMemorySupplierRepository();
    public final InMemoryPurchaseOrderRepository ordenes = new InMemoryPurchaseOrderRepository();
    public final InMemoryProductRepository productos = new InMemoryProductRepository();

    public final SupplierService supplierService = new SupplierService(proveedores, ordenes);
    public final QuotationService quotationService = new QuotationService();
    public final PurchaseOrderService purchaseOrderService = new PurchaseOrderService(proveedores, ordenes);
    public final InventoryService inventoryService = new InventoryService(productos);

    /** Mensaje que el sistema mostraría al usuario tras la última acción. */
    public String mensaje;
    public RuntimeException excepcion;

    /** Ejecuta la acción del paso @Cuando y guarda el mensaje de éxito o el de la excepción. */
    public void ejecutar(Supplier<String> accion) {
        try {
            mensaje = accion.get();
            excepcion = null;
        } catch (RuntimeException e) {
            excepcion = e;
            mensaje = e.getMessage();
        }
    }
}
