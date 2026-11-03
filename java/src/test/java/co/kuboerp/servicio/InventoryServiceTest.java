package co.kuboerp.servicio;

import co.kuboerp.dominio.InsufficientStockException;
import co.kuboerp.dominio.InvalidProductException;
import co.kuboerp.dominio.Product;
import co.kuboerp.repositorio.InMemoryProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

/** Taller 4 · Retiro de inventario: recorre los casos del Scenario Outline con @CsvSource. */
@DisplayName("KuboERP · Inventario de material eléctrico")
class InventoryServiceTest {

    private InventoryService service;

    @BeforeEach
    void setUp() {
        service = new InventoryService(new InMemoryProductRepository());
    }

    @ParameterizedTest(name = "{0}: stock {1}, retiro {2} → final {3} ({4})")
    @CsvSource({
            "CAB-THHN-12,     10, 3, 7, Retiro exitoso",
            "BRK-2X30,         5, 5, 0, Retiro exitoso",
            "TOMA-DOBLE-PT,  2, 5, 2, Stock insuficiente"
    })
    @DisplayName("Retiro de inventario según el esquema Gherkin del Taller 4")
    void deberiaRetirarOLanzarExcepcion(String codigo, int stock, int retiro, int stockFinal, String mensaje) {
        service.register(new Product(codigo, "Producto " + codigo, "Material eléctrico", stock));

        if (retiro > stock) {
            InsufficientStockException error =
                    assertThrows(InsufficientStockException.class, () -> service.retirar(codigo, retiro));
            assertEquals(mensaje, error.getMessage());
        } else {
            service.retirar(codigo, retiro);
            assertEquals(InventoryService.MSG_RETIRO_EXITOSO, mensaje);
        }
        assertEquals(stockFinal, service.stockDe(codigo));
    }

    @Test
    @DisplayName("No debe registrar dos productos con el mismo código")
    void noDeberiaRegistrarCodigoDuplicado() {
        service.register(new Product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 40));

        assertThrows(InvalidProductException.class,
                () -> service.register(new Product("BRK-2X30", "Otro breaker", "Breakers y tableros", 5)));
    }

    @Test
    @DisplayName("No debe registrar un producto sin categoría o con stock negativo")
    void noDeberiaRegistrarProductoInvalido() {
        assertThrows(InvalidProductException.class,
                () -> service.register(new Product("LED-6060-48W", "Panel LED", "", 10)));
        assertThrows(InvalidProductException.class,
                () -> service.register(new Product("LED-6060-48W", "Panel LED", "Iluminación", -1)));
    }
}
