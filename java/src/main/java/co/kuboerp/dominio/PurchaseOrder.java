package co.kuboerp.dominio;

/** Orden de compra (OC) a un proveedor. Estados: PENDIENTE, APROBADA, RECIBIDA, CANCELADA. */
public class PurchaseOrder {
    private final String codigo;
    private final String nitProveedor;
    private final long monto;
    private String estado;

    public PurchaseOrder(String codigo, String nitProveedor, long monto, String estado) {
        this.codigo = codigo;
        this.nitProveedor = nitProveedor;
        this.monto = monto;
        this.estado = estado;
    }

    public String getCodigo() { return codigo; }
    public String getNitProveedor() { return nitProveedor; }
    public long getMonto() { return monto; }
    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }

    public boolean isActiva() {
        return "PENDIENTE".equals(estado) || "APROBADA".equals(estado);
    }
}
