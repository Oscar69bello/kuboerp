package co.kuboerp.dominio;

public class SupplierHasActiveOrdersException extends RuntimeException {
    public SupplierHasActiveOrdersException(String mensaje) { super(mensaje); }
}
