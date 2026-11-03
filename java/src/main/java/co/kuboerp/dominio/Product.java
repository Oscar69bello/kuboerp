package co.kuboerp.dominio;

/** Producto, materia prima o insumo eléctrico del inventario de KuboERP. */
public class Product {
    private final String codigo;
    private final String nombre;
    private final String categoria;
    private int stock;
    private String estado = "DISPONIBLE";

    public Product(String codigo, String nombre, String categoria, int stock) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.categoria = categoria;
        this.stock = stock;
    }

    public String getCodigo() { return codigo; }
    public String getNombre() { return nombre; }
    public String getCategoria() { return categoria; }
    public int getStock() { return stock; }
    public void setStock(int stock) { this.stock = stock; }
    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }
}
