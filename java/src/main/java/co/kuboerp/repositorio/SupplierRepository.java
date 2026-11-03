package co.kuboerp.repositorio;

import co.kuboerp.dominio.Supplier;
import java.util.Optional;

public interface SupplierRepository {
    Supplier save(Supplier proveedor);
    Optional<Supplier> findByNit(String nit);
    Optional<Supplier> findByNombre(String nombre);
    long count();
}
