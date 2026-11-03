package co.kuboerp.servicio;

import co.kuboerp.dominio.InvalidSupplierException;
import co.kuboerp.dominio.Supplier;
import co.kuboerp.dominio.SupplierHasActiveOrdersException;
import co.kuboerp.repositorio.InMemoryPurchaseOrderRepository;
import co.kuboerp.repositorio.PurchaseOrderRepository;
import co.kuboerp.repositorio.SupplierRepository;
import java.util.regex.Pattern;

/** CRUD de proveedores de KuboERP (Taller 1). */
public class SupplierService {
    public static final String MSG_REGISTRADO = "Proveedor registrado exitosamente";
    public static final String MSG_DESACTIVADO = "Proveedor desactivado";

    private static final Pattern NIT = Pattern.compile("\\d{9,10}");
    private static final Pattern CORREO = Pattern.compile("^[\\w.+-]+@[\\w-]+(\\.[\\w-]+)+$");

    private final SupplierRepository proveedores;
    private final PurchaseOrderRepository ordenes;

    public SupplierService(SupplierRepository proveedores) {
        this(proveedores, new InMemoryPurchaseOrderRepository());
    }

    public SupplierService(SupplierRepository proveedores, PurchaseOrderRepository ordenes) {
        this.proveedores = proveedores;
        this.ordenes = ordenes;
    }

    public Supplier createSupplier(Supplier proveedor) {
        if (proveedor.getNit() == null || !NIT.matcher(proveedor.getNit()).matches()) {
            throw new InvalidSupplierException("El NIT no es válido");
        }
        if (proveedor.getNombre() == null || proveedor.getNombre().isBlank()) {
            throw new InvalidSupplierException("El nombre es obligatorio");
        }
        if (proveedor.getCorreo() == null || !CORREO.matcher(proveedor.getCorreo()).matches()) {
            throw new InvalidSupplierException("Formato de correo inválido");
        }
        if (existsByNit(proveedor.getNit())) {
            throw new InvalidSupplierException("El NIT ya está registrado");
        }
        proveedor.setEstado("ACTIVO");
        return proveedores.save(proveedor);
    }

    public boolean existsByNit(String nit) {
        return proveedores.findByNit(nit).isPresent();
    }

    public Supplier findByNit(String nit) {
        return proveedores.findByNit(nit)
                .orElseThrow(() -> new InvalidSupplierException("Proveedor no encontrado"));
    }

    /** Eliminación lógica: el proveedor pasa a INACTIVO si no tiene órdenes de compra activas. */
    public String deleteSupplier(String nit) {
        Supplier proveedor = findByNit(nit);
        if (ordenes.hasActiveOrders(nit)) {
            throw new SupplierHasActiveOrdersException(
                    "No se puede eliminar un proveedor con órdenes de compra activas");
        }
        proveedor.setEstado("INACTIVO");
        proveedores.save(proveedor);
        return MSG_DESACTIVADO;
    }

    public long count() {
        return proveedores.count();
    }
}
