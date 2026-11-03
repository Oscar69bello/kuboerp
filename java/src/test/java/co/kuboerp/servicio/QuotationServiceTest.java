package co.kuboerp.servicio;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

/** Ejercicio 2 · Cálculo del total de una línea de cotización con @CsvSource. */
@DisplayName("KuboERP · Cálculo del total de cotizaciones")
class QuotationServiceTest {

    private QuotationService service;

    @BeforeEach
    void setUp() {
        service = new QuotationService();
    }

    @ParameterizedTest(name = "{0}: {1} × {2} = {3}")
    @CsvSource({
            "'Cable THHN 12 AWG (rollo 100 m)', 285000, 4,  1140000",
            "'Breaker 2x30A',                    48500, 10, 485000",
            "'Panel LED 60x60 48W',              92000, 25, 2300000"
    })
    @DisplayName("Debe calcular precio unitario × cantidad")
    void deberiaCalcularTotalDeLaCotizacion(String producto, long precioUnitario, int cantidad, long totalEsperado) {
        assertEquals(totalEsperado, service.calcularTotal(precioUnitario, cantidad), producto);
    }

    @ParameterizedTest(name = "precio {0}, cantidad {1} → excepción")
    @CsvSource({
            "48500, 0",
            "48500, -3"
    })
    @DisplayName("Debe lanzar excepción cuando la cantidad es cero o negativa")
    void deberiaRechazarCantidadCeroONegativa(long precioUnitario, int cantidad) {
        IllegalArgumentException error = assertThrows(IllegalArgumentException.class,
                () -> service.calcularTotal(precioUnitario, cantidad));
        assertEquals("La cantidad debe ser mayor que cero", error.getMessage());
    }
}
