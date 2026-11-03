package co.kuboerp.repositorio;

import co.kuboerp.dominio.PurchaseOrder;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

public class InMemoryPurchaseOrderRepository implements PurchaseOrderRepository {
    private final Map<String, PurchaseOrder> datos = new LinkedHashMap<>();

    @Override
    public PurchaseOrder save(PurchaseOrder orden) {
        datos.put(orden.getCodigo(), orden);
        return orden;
    }

    @Override
    public Optional<PurchaseOrder> findByCodigo(String codigo) {
        return Optional.ofNullable(datos.get(codigo));
    }

    @Override
    public boolean hasActiveOrders(String nitProveedor) {
        return datos.values().stream()
                .anyMatch(o -> o.getNitProveedor().equals(nitProveedor) && o.isActiva());
    }
}
