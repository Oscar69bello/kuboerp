using KuboERP.Web.Data;
using KuboERP.Web.Models;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Controllers;

public class ProveedoresController : BaseController
{
    private readonly ProveedorService servicio;
    private readonly KuboDbContext db;

    public ProveedoresController(ProveedorService servicio, KuboDbContext db)
    {
        this.servicio = servicio;
        this.db = db;
    }

    public async Task<IActionResult> Index(string? buscar, string? estado)
    {
        ViewBag.Buscar = buscar;
        ViewBag.Estado = estado;
        return View(await servicio.ListarAsync(string.IsNullOrWhiteSpace(buscar) ? null : buscar, estado));
    }

    public async Task<IActionResult> Detalle(int id)
    {
        try
        {
            var p = await servicio.BuscarAsync(id);
            ViewBag.Ordenes = await db.Ordenes.Where(o => o.ProveedorId == id).OrderByDescending(o => o.Fecha).ToListAsync();
            ViewBag.Cotizaciones = await db.Cotizaciones.Include(c => c.Solicitud).Where(c => c.ProveedorId == id).ToListAsync();
            return View(p);
        }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    public IActionResult Crear() => View("Formulario", new Proveedor());

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(Proveedor p)
    {
        if (!ModelState.IsValid) return View("Formulario", p);
        try
        {
            await servicio.CrearAsync(p);
            Exito($"Proveedor {p.Nombre} registrado exitosamente");
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
    public async Task<IActionResult> Editar(Proveedor p)
    {
        ModelState.Remove(nameof(Proveedor.Nit));
        if (!ModelState.IsValid) return View("Formulario", p);
        try
        {
            await servicio.ActualizarAsync(p);
            Exito($"Proveedor {p.Nombre} actualizado");
            return RedirectToAction(nameof(Detalle), new { id = p.Id });
        }
        catch (ReglaNegocioException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View("Formulario", p);
        }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Eliminar(int id) =>
        Ejecutar(() => servicio.EliminarAsync(id), () => RedirectToAction(nameof(Index)));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Reactivar(int id) =>
        Ejecutar(async () => { await servicio.ReactivarAsync(id); return "Proveedor reactivado"; },
                 () => RedirectToAction(nameof(Detalle), new { id }));
}
