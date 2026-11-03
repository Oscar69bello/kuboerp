package co.kuboerp.repositorio;

import co.kuboerp.dominio.Product;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class InMemoryProductRepository implements ProductRepository {
    private final Map<String, Product> datos = new LinkedHashMap<>();
    private final Map<String, List<String>> kardex = new LinkedHashMap<>();

    @Override
    public Product save(Product producto) {
        datos.put(producto.getCodigo(), producto);
        return producto;
    }

    @Override
    public Optional<Product> findByCodigo(String codigo) {
        return Optional.ofNullable(datos.get(codigo));
    }

    @Override
    public void registrarMovimiento(String codigo, String tipo, int cantidad) {
        kardex.computeIfAbsent(codigo, c -> new ArrayList<>()).add(tipo + ":" + cantidad);
    }

    @Override
    public List<String> historial(String codigo) {
        return kardex.getOrDefault(codigo, List.of());
    }
}
