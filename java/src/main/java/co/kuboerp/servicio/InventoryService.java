package co.kuboerp.servicio;

import co.kuboerp.dominio.InsufficientStockException;
import co.kuboerp.dominio.InvalidProductException;
import co.kuboerp.dominio.Product;
import co.kuboerp.repositorio.ProductRepository;

/** Inventario de productos, materia prima e insumos eléctricos (Taller 4). */
public class InventoryService {
    public static final String MSG_RETIRO_EXITOSO = "Retiro exitoso";
    public static final String MSG_STOCK_INSUFICIENTE = "Stock insuficiente";

    private final ProductRepository productos;

    public InventoryService(ProductRepository productos) {
        this.productos = productos;
    }

    public Product register(Product producto) {
        if (producto.getCodigo() == null || producto.getCodigo().isBlank()) {
            throw new InvalidProductException("El código es obligatorio");
        }
        if (productos.findByCodigo(producto.getCodigo()).isPresent()) {
            throw new InvalidProductException("El código ya está registrado");
        }
        if (producto.getStock() < 0) {
            throw new InvalidProductException("El stock inicial no puede ser negativo");
        }
        if (producto.getCategoria() == null || producto.getCategoria().isBlank()) {
            throw new InvalidProductException("La categoría es obligatoria");
        }
        return productos.save(producto);
    }

    public int registrarEntrada(String codigo, int cantidad) {
        if (cantidad <= 0) {
            throw new InvalidProductException("La cantidad debe ser mayor que cero");
        }
        Product producto = buscar(codigo);
        producto.setStock(producto.getStock() + cantidad);
        productos.save(producto);
        productos.registrarMovimiento(codigo, "ENTRADA", cantidad);
        return producto.getStock();
    }

    public int retirar(String codigo, int cantidad) {
        Product producto = buscar(codigo);
        if (cantidad > producto.getStock()) {
            throw new InsufficientStockException(MSG_STOCK_INSUFICIENTE);
        }
        producto.setStock(producto.getStock() - cantidad);
        productos.save(producto);
        productos.registrarMovimiento(codigo, "SALIDA", cantidad);
        return producto.getStock();
    }

    public int stockDe(String codigo) {
        return buscar(codigo).getStock();
    }

    public int movimientos(String codigo) {
        return productos.historial(codigo).size();
    }

    private Product buscar(String codigo) {
        return productos.findByCodigo(codigo)
                .orElseThrow(() -> new InvalidProductException("Producto no encontrado"));
    }
}
