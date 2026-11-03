package co.kuboerp.servicio;

import co.kuboerp.dominio.InvalidQuotationException;
import co.kuboerp.dominio.Quotation;
import java.util.ArrayList;
import java.util.List;

/** Cotizaciones de material eléctrico (Ejercicios 2 y 4). */
public class QuotationService {
    public static final String MSG_REGISTRADA = "Cotización registrada";

    private final List<Quotation> cotizaciones = new ArrayList<>();

    /** Total de una línea de cotización = precio unitario × cantidad, en pesos colombianos. */
    public long calcularTotal(long precioUnitario, int cantidad) {
        if (cantidad <= 0) {
            throw new IllegalArgumentException("La cantidad debe ser mayor que cero");
        }
        if (precioUnitario <= 0) {
            throw new IllegalArgumentException("El precio unitario debe ser mayor que cero");
        }
        return Math.multiplyExact(precioUnitario, cantidad);
    }

    public Quotation registrar(String solicitud, String nitProveedor, long monto) {
        if (monto <= 0) {
            throw new InvalidQuotationException("El monto debe ser mayor que cero");
        }
        Quotation cotizacion = new Quotation(solicitud, nitProveedor, monto);
        cotizaciones.add(cotizacion);
        return cotizacion;
    }

    public int total() {
        return cotizaciones.size();
    }
}
