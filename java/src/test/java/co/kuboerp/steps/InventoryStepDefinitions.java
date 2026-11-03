package co.kuboerp.steps;

import co.kuboerp.dominio.Product;
import co.kuboerp.servicio.InventoryService;
import io.cucumber.java.es.Cuando;
import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Taller 4 · Entradas y retiros de inventario. */
public class InventoryStepDefinitions {
    /** Catálogo de los mockups de KuboERP: código → {nombre, categoría}. */
    private static final Map<String, String[]> CATALOGO = Map.of(
            "CAB-THHN-12", new String[]{"Cable THHN 12 AWG (rollo 100 m)", "Cables"},
            "BRK-2X30", new String[]{"Breaker 2x30A", "Breakers y tableros"},
            "LED-6060-48W", new String[]{"Panel LED 60x60 48W", "Iluminación"},
            "TOMA-DOBLE-PT", new String[]{"Toma doble con polo a tierra", "Interruptores y tomas"});

    private final Contexto ctx;
    private String codigo;

    public InventoryStepDefinitions(Contexto ctx) {
        this.ctx = ctx;
    }

    @Dado("que el producto {string} tiene stock actual {int}")
    public void queElProductoTieneStockActual(String codigo, int stock) {
        registrar(codigo, stock);
    }

    @Dado("que el producto {string} tiene stock {int}")
    public void queElProductoTieneStock(String codigo, int stock) {
        registrar(codigo, stock);
    }

    @Cuando("se registra una entrada de {int} unidades")
    public void seRegistraUnaEntrada(int cantidad) {
        ctx.ejecutar(() -> {
            ctx.inventoryService.registrarEntrada(codigo, cantidad);
            return "Entrada registrada";
        });
    }

    @Cuando("se intenta retirar {int} unidades")
    public void seIntentaRetirar(int cantidad) {
        retirar(cantidad);
    }

    @Cuando("se retiran {int} unidades")
    public void seRetiran(int cantidad) {
        retirar(cantidad);
    }

    @Entonces("el stock final debe ser {int}")
    public void elStockFinalDebeSer(int esperado) {
        assertEquals(esperado, ctx.inventoryService.stockDe(codigo));
    }

    @Entonces("el stock final es {int}")
    public void elStockFinalEs(int esperado) {
        elStockFinalDebeSer(esperado);
    }

    @Entonces("el stock permanece en {int}")
    public void elStockPermaneceEn(int esperado) {
        elStockFinalDebeSer(esperado);
    }

    @Entonces("el movimiento queda registrado en el historial")
    public void elMovimientoQuedaRegistrado() {
        assertEquals(1, ctx.inventoryService.movimientos(codigo));
    }

    private void registrar(String codigo, int stock) {
        this.codigo = codigo;
        String[] datos = CATALOGO.getOrDefault(codigo, new String[]{codigo, "Material eléctrico"});
        ctx.inventoryService.register(new Product(codigo, datos[0], datos[1], stock));
    }

    private void retirar(int cantidad) {
        ctx.ejecutar(() -> {
            ctx.inventoryService.retirar(codigo, cantidad);
            return InventoryService.MSG_RETIRO_EXITOSO;
        });
    }
}
