package co.kuboerp.repositorio;

import co.kuboerp.dominio.Product;
import java.util.List;
import java.util.Optional;

public interface ProductRepository {
    Product save(Product producto);
    Optional<Product> findByCodigo(String codigo);
    void registrarMovimiento(String codigo, String tipo, int cantidad);
    List<String> historial(String codigo);
}
