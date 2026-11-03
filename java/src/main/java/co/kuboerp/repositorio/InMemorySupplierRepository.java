package co.kuboerp.repositorio;

import co.kuboerp.dominio.Supplier;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

public class InMemorySupplierRepository implements SupplierRepository {
    private final Map<String, Supplier> datos = new LinkedHashMap<>();
    private long secuencia = 0;

    @Override
    public Supplier save(Supplier proveedor) {
        if (proveedor.getId() == null) {
            proveedor.setId(++secuencia);
        }
        datos.put(proveedor.getNit(), proveedor);
        return proveedor;
    }

    @Override
    public Optional<Supplier> findByNit(String nit) {
        return Optional.ofNullable(datos.get(nit));
    }

    @Override
    public Optional<Supplier> findByNombre(String nombre) {
        return datos.values().stream().filter(p -> p.getNombre().equals(nombre)).findFirst();
    }

    @Override
    public long count() {
        return datos.size();
    }
}
