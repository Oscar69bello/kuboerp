using KuboERP.Web.Models;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace KuboERP.Web.Controllers;

public class EmpleadosController : BaseController
{
    private readonly EmpleadoService servicio;
    public EmpleadosController(EmpleadoService servicio) => this.servicio = servicio;

    public async Task<IActionResult> Index(string? cargo, string estado = "ACTIVO")
    {
        ViewBag.Cargo = cargo;
        ViewBag.EstadoFiltro = estado;
        return View(await servicio.ListarAsync(cargo, estado));
    }

    public IActionResult Crear() => View("Formulario", new Empleado { SalarioBase = ParametrosNomina.Smmlv });

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(Empleado e)
    {
        if (!ModelState.IsValid) return View("Formulario", e);
        try
        {
            await servicio.CrearAsync(e);
            Exito($"Empleado {e.Nombre} registrado");
            return RedirectToAction(nameof(Index));
        }
        catch (ReglaNegocioException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View("Formulario", e);
        }
    }

    public async Task<IActionResult> Editar(int id)
    {
        try { return View("Formulario", await servicio.BuscarAsync(id)); }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Editar(Empleado e)
    {
        ModelState.Remove(nameof(Empleado.Cedula));
        if (!ModelState.IsValid) return View("Formulario", e);
        try
        {
            await servicio.ActualizarAsync(e);
            Exito($"Empleado {e.Nombre} actualizado");
            return RedirectToAction(nameof(Index));
        }
        catch (ReglaNegocioException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View("Formulario", e);
        }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Desvincular(int id) =>
        Ejecutar(async () => { await servicio.DesvincularAsync(id); return "Empleado desvinculado: ya no entra en la nómina"; },
                 () => RedirectToAction(nameof(Index)));
}

public class NominaController : BaseController
{
    private readonly NominaService nomina;
    private readonly EmpleadoService empleados;

    public NominaController(NominaService nomina, EmpleadoService empleados)
    {
        this.nomina = nomina;
        this.empleados = empleados;
    }

    public async Task<IActionResult> Index(string? periodo)
    {
        var periodos = await nomina.PeriodosAsync();
        periodo ??= periodos.FirstOrDefault();
        ViewBag.Periodos = periodos;
        ViewBag.Periodo = periodo;
        return View(periodo is null ? new List<DesprendibleNomina>() : await nomina.DesprendiblesAsync(periodo));
    }

    public async Task<IActionResult> Liquidar(string? periodo)
    {
        ViewBag.Periodo = periodo ?? DateTime.Today.ToString("yyyy-MM");
        return View(await empleados.ListarAsync(null));
    }

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Liquidar(string periodo, List<NovedadNomina> novedades)
    {
        try
        {
            int n = await nomina.LiquidarAsync(periodo, novedades);
            Exito($"Nómina de {periodo} liquidada para {n} empleados");
            return RedirectToAction(nameof(Index), new { periodo });
        }
        catch (ReglaNegocioException ex)
        {
            Error(ex.Message);
            return RedirectToAction(nameof(Liquidar), new { periodo });
        }
    }

    public async Task<IActionResult> Desprendible(int id)
    {
        try { return View(await nomina.DesprendibleAsync(id)); }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }
}
