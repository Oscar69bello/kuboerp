package co.kuboerp.dominio;

public class InvalidProductException extends RuntimeException {
    public InvalidProductException(String mensaje) { super(mensaje); }
}
