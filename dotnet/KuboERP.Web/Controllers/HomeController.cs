using System.Diagnostics;
using KuboERP.Web.Data;
using KuboERP.Web.Models;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Controllers;

public class TableroViewModel
{
    public int ProveedoresActivos { get; set; }
    public decimal PresupuestoDisponible { get; set; }
    public int ProductosActivos { get; set; }
    public decimal ValorInventario { get; set; }
    public int OrdenesPendientes { get; set; }
    public int OrdenesAprobadas { get; set; }
    public decimal ComprasDelMes { get; set; }
    public int EmpleadosActivos { get; set; }
    public decimal CostoUltimaNomina { get; set; }
    public string? UltimoPeriodo { get; set; }
    public int SolicitudesAbiertas { get; set; }
    public List<Producto> Criticos { get; set; } = new();
    public List<OrdenCompra> UltimasOrdenes { get; set; } = new();
    public List<MovimientoInventario> UltimosMovimientos { get; set; } = new();
    public List<(string Categoria, decimal Valor)> InventarioPorCategoria { get; set; } = new();
}

public class HomeController : BaseController
{
    private readonly KuboDbContext db;
    private readonly InventarioService inventario;

    public HomeController(KuboDbContext db, InventarioService inventario)
    {
        this.db = db;
        this.inventario = inventario;
    }

    public async Task<IActionResult> Index()
    {
        var hoy = DateTime.Today;
        var productos = await db.Productos.Where(p => p.Activo).ToListAsync();
        var ultimoPeriodo = await db.Desprendibles.MaxAsync(d => (string?)d.Periodo);
        var nomina = ultimoPeriodo is null ? new List<DesprendibleNomina>()
            : await db.Desprendibles.Where(d => d.Periodo == ultimoPeriodo).ToListAsync();

        var vm = new TableroViewModel
        {
            ProveedoresActivos = await db.Proveedores.CountAsync(p => p.Estado == EstadosProveedor.Activo),
            PresupuestoDisponible = await db.Proveedores.Where(p => p.Estado == EstadosProveedor.Activo).SumAsync(p => p.Presupuesto),
            ProductosActivos = productos.Count,
            ValorInventario = productos.Sum(p => p.Stock * p.PrecioUnitario),
            OrdenesPendientes = await db.Ordenes.CountAsync(o => o.Estado == EstadosOrden.Pendiente),
            OrdenesAprobadas = await db.Ordenes.CountAsync(o => o.Estado == EstadosOrden.Aprobada),
            ComprasDelMes = await db.Ordenes
                .Where(o => o.Fecha.Year == hoy.Year && o.Fecha.Month == hoy.Month && o.Estado != EstadosOrden.Cancelada)
                .SumAsync(o => o.Monto),
            EmpleadosActivos = await db.Empleados.CountAsync(e => e.Estado == "ACTIVO"),
            CostoUltimaNomina = nomina.Sum(d => d.CostoEmpleador),
            UltimoPeriodo = ultimoPeriodo,
            SolicitudesAbiertas = await db.Solicitudes.CountAsync(s => s.Estado == "ABIERTA"),
            Criticos = await inventario.CriticosAsync(),
            UltimasOrdenes = await db.Ordenes.Include(o => o.Proveedor).OrderByDescending(o => o.Fecha).Take(5).ToListAsync(),
            UltimosMovimientos = await inventario.MovimientosAsync(null, 6),
            InventarioPorCategoria = productos.GroupBy(p => p.Categoria)
                .Select(g => (g.Key, g.Sum(p => p.Stock * p.PrecioUnitario)))
                .OrderByDescending(x => x.Item2).ToList()
        };
        return View(vm);
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error() =>
        View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
}
