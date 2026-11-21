using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace KuboERP.Web.Controllers;

/// <summary>Muestra al usuario el resultado de una operación o la regla de negocio que impidió hacerla.</summary>
public abstract class BaseController : Controller
{
    protected void Exito(string mensaje) => TempData["Exito"] = mensaje;
    protected void Error(string mensaje) => TempData["Error"] = mensaje;

    protected async Task<IActionResult> Ejecutar(Func<Task<string>> accion, Func<IActionResult> destino)
    {
        try { Exito(await accion()); }
        catch (ReglaNegocioException ex) { Error(ex.Message); }
        return destino();
    }
}
