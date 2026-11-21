using KuboERP.Web.Data;
using KuboERP.Web.Models;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Controllers;

public class CotizacionesController : BaseController
{
    private readonly CotizacionService servicio;
    private readonly KuboDbContext db;

    public CotizacionesController(CotizacionService servicio, KuboDbContext db)
    {
        this.servicio = servicio;
        this.db = db;
    }

    public async Task<IActionResult> Index()
    {
        ViewBag.SiguienteCodigo = $"SOL-2026-{await db.Solicitudes.CountAsync() + 1:000}";
        return View(await servicio.ListarSolicitudesAsync());
    }

    public async Task<IActionResult> Solicitud(int id)
    {
        try
        {
            ViewBag.Proveedores = await db.Proveedores.Where(p => p.Estado == EstadosProveedor.Activo).OrderBy(p => p.Nombre).ToListAsync();
            return View(await servicio.BuscarSolicitudAsync(id));
        }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Abrir(string codigo, string descripcion) =>
        Ejecutar(async () => { await servicio.AbrirSolicitudAsync(codigo, descripcion); return $"Solicitud {codigo} abierta"; },
                 () => RedirectToAction(nameof(Index)));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Registrar(int solicitudId, int proveedorId, decimal monto, int diasEntrega) =>
        Ejecutar(async () => { await servicio.RegistrarAsync(solicitudId, proveedorId, monto, diasEntrega); return "Cotización registrada en estado RECIBIDA"; },
                 () => RedirectToAction(nameof(Solicitud), new { id = solicitudId }));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Seleccionar(int id, int solicitudId) =>
        Ejecutar(async () =>
        {
            var c = await servicio.SeleccionarAsync(id);
            return $"Cotización {c.Codigo} seleccionada. Las demás quedan rechazadas y la solicitud se cierra.";
        }, () => RedirectToAction(nameof(Solicitud), new { id = solicitudId }));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Anular(int id, int solicitudId) =>
        Ejecutar(async () => { await servicio.AnularAsync(id); return "Cotización anulada"; },
                 () => RedirectToAction(nameof(Solicitud), new { id = solicitudId }));
}

public class OrdenesController : BaseController
{
    private readonly OrdenCompraService servicio;
    private readonly KuboDbContext db;

    public OrdenesController(OrdenCompraService servicio, KuboDbContext db)
    {
        this.servicio = servicio;
        this.db = db;
    }

    public async Task<IActionResult> Index(string? estado)
    {
        ViewBag.Estado = estado;
        return View(await servicio.ListarAsync(estado));
    }

    public async Task<IActionResult> Detalle(int id)
    {
        try { return View(await servicio.BuscarAsync(id)); }
        catch (ReglaNegocioException ex) { Error(ex.Message); return RedirectToAction(nameof(Index)); }
    }

    public async Task<IActionResult> Crear(int? proveedorId)
    {
        await CargarListas();
        ViewBag.ProveedorId = proveedorId;
        ViewBag.Codigo = await servicio.SiguienteCodigoAsync();
        return View();
    }

    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(int proveedorId, int[] productoId, int[] cantidad, decimal[] precio)
    {
        var lineas = productoId.Select((p, i) => new LineaNueva(p,
            i < cantidad.Length ? cantidad[i] : 0, i < precio.Length ? precio[i] : 0));
        try
        {
            var o = await servicio.CrearAsync(proveedorId, lineas);
            Exito($"Orden {o.Codigo} creada por {Formato.Pesos(o.Monto)} en estado PENDIENTE");
            return RedirectToAction(nameof(Detalle), new { id = o.Id });
        }
        catch (ReglaNegocioException ex)
        {
            Error(ex.Message);
            return RedirectToAction(nameof(Crear), new { proveedorId });
        }
    }

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Aprobar(int id) =>
        Ejecutar(async () => { await servicio.AprobarAsync(id); return "Orden aprobada: el monto se descontó del presupuesto del proveedor"; },
                 () => RedirectToAction(nameof(Detalle), new { id }));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Recibir(int id) =>
        Ejecutar(async () => { await servicio.RecibirAsync(id); return "Mercancía recibida: se generaron las entradas de inventario"; },
                 () => RedirectToAction(nameof(Detalle), new { id }));

    [HttpPost, ValidateAntiForgeryToken]
    public Task<IActionResult> Cancelar(int id, string? justificacion) =>
        Ejecutar(async () => { await servicio.CancelarAsync(id, justificacion); return "Orden cancelada"; },
                 () => RedirectToAction(nameof(Detalle), new { id }));

    private async Task CargarListas()
    {
        ViewBag.Proveedores = await db.Proveedores.Where(p => p.Estado == EstadosProveedor.Activo).OrderBy(p => p.Nombre).ToListAsync();
        ViewBag.Productos = await db.Productos.Where(p => p.Activo).OrderBy(p => p.Nombre).ToListAsync();
    }
}
