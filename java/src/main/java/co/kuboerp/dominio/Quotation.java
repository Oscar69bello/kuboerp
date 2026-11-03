package co.kuboerp.dominio;

/** Cotización (COT) de un proveedor para una solicitud de compra. */
public class Quotation {
    private final String solicitud;
    private final String nitProveedor;
    private final long monto;

    public Quotation(String solicitud, String nitProveedor, long monto) {
        this.solicitud = solicitud;
        this.nitProveedor = nitProveedor;
        this.monto = monto;
    }

    public String getSolicitud() { return solicitud; }
    public String getNitProveedor() { return nitProveedor; }
    public long getMonto() { return monto; }
}
