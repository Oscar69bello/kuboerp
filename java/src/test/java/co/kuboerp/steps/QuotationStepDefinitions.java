package co.kuboerp.steps;

import co.kuboerp.servicio.QuotationService;
import io.cucumber.java.es.Cuando;
import io.cucumber.java.es.Dado;
import io.cucumber.java.es.Entonces;

import static org.junit.jupiter.api.Assertions.*;

/** Ejercicio 4 · Rechazar cotización con monto cero. */
public class QuotationStepDefinitions {
    private final Contexto ctx;
    private String solicitud;

    public QuotationStepDefinitions(Contexto ctx) {
        this.ctx = ctx;
    }

    @Dado("que existe una solicitud de compra {string} para {string} en estado {string}")
    public void queExisteUnaSolicitudDeCompra(String codigo, String producto, String estado) {
        solicitud = codigo;
        assertEquals("ABIERTA", estado);
    }

    @Cuando("el proveedor con NIT {string} registra la cotización {string} por {long}")
    public void elProveedorRegistraLaCotizacion(String nit, String cotizacion, long monto) {
        // Se captura la excepción para que el paso @Entonces verifique el mensaje.
        ctx.ejecutar(() -> {
            ctx.quotationService.registrar(solicitud, nit, monto);
            return QuotationService.MSG_REGISTRADA;
        });
    }

    @Entonces("no se registra la cotización")
    public void noSeRegistraLaCotizacion() {
        assertNotNull(ctx.excepcion);
        assertEquals(0, ctx.quotationService.total());
    }
}
