package co.kuboerp.steps;

import io.cucumber.java.es.Entonces;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Pasos comunes a todas las características: verifican el mensaje que muestra KuboERP. */
public class MensajeSteps {
    private final Contexto ctx;

    public MensajeSteps(Contexto ctx) {
        this.ctx = ctx;
    }

    @Entonces("el sistema muestra {string}")
    public void elSistemaMuestra(String esperado) {
        assertEquals(esperado, ctx.mensaje);
    }

    @Entonces("el sistema responde {string}")
    public void elSistemaResponde(String esperado) {
        assertEquals(esperado, ctx.mensaje);
    }

    @Entonces("el sistema confirma {string}")
    public void elSistemaConfirma(String esperado) {
        assertEquals(esperado, ctx.mensaje);
    }
}
