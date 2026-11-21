using KuboERP.Web.Models;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;

namespace KuboERP.Web.Controllers;

public class InventarioController : BaseController
{
    private readonly InventarioService servicio;
    public InventarioController(InventarioService servicio) => this.servicio = servicio;

    public async Task<IActionResult> Index(string? buscar, string? categoria, bool criticos = false, bool inactivos = false)
    {
        ViewBag.Buscar = buscar;
        ViewBag.Categoria = categoria;
        ViewBag.Criticos = criticos;
        ViewBag.Inactivos = inactivos;
        ViewBag.TotalCriticos = (await servicio.CriticosAsync()).Count;
        return View(await servicio.ListarAsync(string.IsNullOrWhiteSpace(buscar) ? null : buscar, categoria, criticos, inactivos));
    }

    public async Task<IActionResult> Detalle(int id)
    {
        try
        {
            var p = await servicio.BuscarAsync(id);
            ViewBag.Movimientos = await servicio.MovimientosAsync(id);
            return View(p);
        }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    public async Task<IActionResult> Movimientos() => View(await servicio.MovimientosAsync(null, 100));

    public IActionResult Crear() => View("Formulario", new Producto { Categoria = InventarioService.Categorias[0] });

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(Producto p)
    {
        if (!ModelState.IsValid) return View("Formulario", p);
        try
        {
            await servicio.CrearAsync(p);
            Exito($"Producto {p.Codigo} registrado");
            return RedirectToAction(nameof(Index));
        }
        catch (ReglaNegocioException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View("Formulario", p);
        }
    }

    public async Task<IActionResult> Editar(int id)
    {
        try { return View("Formulario", await servicio.BuscarAsync(id)); }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Editar(Producto p)
    {
        ModelState.Remove(nameof(Producto.Codigo));
        ModelState.Remove(nameof(Producto.Stock));
        if (!ModelState.IsValid) return View("Formulario", p);
        try
        {
            await servicio.ActualizarAsync(p);
            Exito($"Producto {p.Nombre} actualizado");
            return RedirectToAction(nameof(Detalle), new { id = p.Id });
        }
        catch (ReglaNegocioException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View("Formulario", p);
        }
    }

    /// <summary>tipo = "entrada" o "salida".</summary>
    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Mover(int id, string tipo, int cantidad, string? detalle, string? volver) =>
        Ejecutar(() => servicio.MoverAsync(id, tipo == "salida" ? -Math.Abs(cantidad) : Math.Abs(cantidad), detalle),
                 () => volver == "lista" ? RedirectToAction(nameof(Index)) : RedirectToAction(nameof(Detalle), new { id }));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Inactivar(int id) =>
        Ejecutar(async () => { await servicio.InactivarAsync(id); return "Producto inactivado"; },
                 () => RedirectToAction(nameof(Detalle), new { id }));
}
