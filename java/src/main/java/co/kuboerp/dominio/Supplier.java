package co.kuboerp.dominio;

/** Proveedor de material eléctrico (módulo Compras de KuboERP). */
public class Supplier {
    private Long id;
    private final String nit;
    private final String nombre;
    private final String correo;
    private String estado = "ACTIVO";
    private long presupuestoDisponible;

    public Supplier(String nit, String nombre, String correo) {
        this.nit = nit;
        this.nombre = nombre;
        this.correo = correo;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getNit() { return nit; }
    public String getNombre() { return nombre; }
    public String getCorreo() { return correo; }
    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }
    public long getPresupuestoDisponible() { return presupuestoDisponible; }
    public void setPresupuestoDisponible(long presupuesto) { this.presupuestoDisponible = presupuesto; }
}
