using Microsoft.AspNetCore.Html;

namespace KuboERP.Web.Services;

/// <summary>Ayudas de presentación para las vistas.</summary>
public static class Ui
{
    public static IHtmlContent Estado(string estado)
    {
        var clase = estado switch
        {
            "ACTIVO" or "APROBADA" or "SELECCIONADA" or "ABIERTA" => "ok",
            "PENDIENTE" or "RECIBIDA" => "pend",
            "RECIBIDA_OC" => "info",
            "INACTIVO" or "CANCELADA" or "RECHAZADA" or "ANULADA" or "RETIRADO" => "off",
            "CERRADA" => "info",
            _ => "info"
        };
        return new HtmlString($"<span class=\"estado estado-{clase}\">{estado}</span>");
    }

    /// <summary>Estado de una orden: RECIBIDA es el estado final feliz y se muestra en azul.</summary>
    public static IHtmlContent EstadoOrden(string estado) =>
        estado == "RECIBIDA" ? new HtmlString("<span class=\"estado estado-info\">RECIBIDA</span>") : Estado(estado);

    public static IHtmlContent Movimiento(string tipo) =>
        new HtmlString($"<span class=\"estado estado-{(tipo == "ENTRADA" ? "ok" : "pend")}\">{tipo}</span>");

    public static string Pesos(decimal v) => Formato.Pesos(v);
    public static string Num(decimal v) => Formato.Numero(v);
    public static string Fecha(DateTime f) => f.ToString("dd MMM yyyy", new System.Globalization.CultureInfo("es-CO"));
    public static string FechaHora(DateTime f) => f.ToString("dd MMM yyyy HH:mm", new System.Globalization.CultureInfo("es-CO"));

    public static string Periodo(string periodo)
    {
        if (!DateTime.TryParseExact(periodo + "-01", "yyyy-MM-dd", null, System.Globalization.DateTimeStyles.None, out var f)) return periodo;
        var texto = f.ToString("MMMM yyyy", new System.Globalization.CultureInfo("es-CO"));
        return char.ToUpper(texto[0]) + texto[1..];
    }
}
