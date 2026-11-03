package co.kuboerp.repositorio;

import co.kuboerp.dominio.PurchaseOrder;
import java.util.Optional;

public interface PurchaseOrderRepository {
    PurchaseOrder save(PurchaseOrder orden);
    Optional<PurchaseOrder> findByCodigo(String codigo);
    boolean hasActiveOrders(String nitProveedor);
}
