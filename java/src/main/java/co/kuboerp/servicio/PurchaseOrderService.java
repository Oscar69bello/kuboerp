package co.kuboerp.servicio;

import co.kuboerp.dominio.PurchaseOrder;
import co.kuboerp.dominio.PurchaseOrderException;
import co.kuboerp.dominio.Supplier;
import co.kuboerp.repositorio.PurchaseOrderRepository;
import co.kuboerp.repositorio.SupplierRepository;

/** Aprobación de órdenes de compra contra el presupuesto del proveedor (Taller 3). */
public class PurchaseOrderService {
    private final SupplierRepository proveedores;
    private final PurchaseOrderRepository ordenes;

    public PurchaseOrderService(SupplierRepository proveedores, PurchaseOrderRepository ordenes) {
        this.proveedores = proveedores;
        this.ordenes = ordenes;
    }

    public PurchaseOrder approve(String codigo) {
        PurchaseOrder orden = ordenes.findByCodigo(codigo)
                .orElseThrow(() -> new PurchaseOrderException("Orden no encontrada"));
        if ("APROBADA".equals(orden.getEstado())) {
            throw new PurchaseOrderException("La orden ya está aprobada");
        }
        Supplier proveedor = proveedores.findByNit(orden.getNitProveedor())
                .orElseThrow(() -> new PurchaseOrderException("Proveedor no encontrado"));
        if (orden.getMonto() > proveedor.getPresupuestoDisponible()) {
            throw new PurchaseOrderException("Presupuesto insuficiente");
        }
        proveedor.setPresupuestoDisponible(proveedor.getPresupuestoDisponible() - orden.getMonto());
        proveedores.save(proveedor);
        orden.setEstado("APROBADA");
        return ordenes.save(orden);
    }
}
