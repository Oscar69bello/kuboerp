using KuboERP.Web.Data;
using KuboERP.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Services;

// ============================ INVENTARIO (EP07) ============================

public class InventarioService
{
    public static readonly string[] Categorias =
        { "Cableado", "Protección", "Iluminación", "Tableros", "Herramientas", "Tubería y accesorios" };

    private readonly KuboDbContext db;
    public InventarioService(KuboDbContext db) => this.db = db;

    public Task<List<Producto>> ListarAsync(string? buscar, string? categoria, bool soloCriticos, bool incluirInactivos) =>
        db.Productos
          .Where(p => incluirInactivos || p.Activo)
          .Where(p => buscar == null || p.Nombre.Contains(buscar) || p.Codigo.Contains(buscar))
          .Where(p => categoria == null || p.Categoria == categoria)
          .Where(p => !soloCriticos || (p.StockMinimo > 0 && p.Stock <= p.StockMinimo))
          .OrderBy(p => p.Categoria).ThenBy(p => p.Nombre).ToListAsync();

    /// <summary>Productos en stock crítico, del más urgente al menos urgente.</summary>
    public async Task<List<Producto>> CriticosAsync()
    {
        var criticos = await db.Productos.Where(p => p.Activo && p.StockMinimo > 0 && p.Stock <= p.StockMinimo).ToListAsync();
        return criticos.OrderBy(p => (double)p.Stock / p.StockMinimo).ToList();
    }

    public async Task<Producto> BuscarAsync(int id) =>
        await db.Productos.FindAsync(id) ?? throw new ReglaNegocioException("Producto no encontrado");

    public Task<List<MovimientoInventario>> MovimientosAsync(int? productoId, int cantidad = 50) =>
        db.Movimientos.Include(m => m.Producto)
          .Where(m => productoId == null || m.ProductoId == productoId)
          .OrderByDescending(m => m.Fecha).ThenByDescending(m => m.Id).Take(cantidad).ToListAsync();

    public async Task CrearAsync(Producto p)
    {
        if (string.IsNullOrWhiteSpace(p.Codigo)) throw new ReglaNegocioException("El código es obligatorio");
        if (string.IsNullOrWhiteSpace(p.Categoria)) throw new ReglaNegocioException("La categoría es obligatoria");
        if (p.Stock < 0) throw new ReglaNegocioException("El stock inicial no puede ser negativo");
        if (p.StockMinimo < 0) throw new ReglaNegocioException("El stock mínimo no puede ser negativo");
        p.Codigo = p.Codigo.Trim().ToUpper();
        if (await db.Productos.AnyAsync(x => x.Codigo == p.Codigo))
            throw new ReglaNegocioException("El código ya está registrado");
        p.Activo = true;
        db.Productos.Add(p);
        if (p.Stock > 0)
            db.Movimientos.Add(new MovimientoInventario
                { Producto = p, Tipo = "ENTRADA", Cantidad = p.Stock, StockResultante = p.Stock, Detalle = "Stock inicial" });
        await db.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Producto cambios)
    {
        var p = await BuscarAsync(cambios.Id);
        if (string.IsNullOrWhiteSpace(cambios.Nombre)) throw new ReglaNegocioException("El nombre es obligatorio");
        if (string.IsNullOrWhiteSpace(cambios.Categoria)) throw new ReglaNegocioException("La categoría es obligatoria");
        if (cambios.StockMinimo < 0) throw new ReglaNegocioException("El stock mínimo no puede ser negativo");
        p.Nombre = cambios.Nombre.Trim();
        p.Categoria = cambios.Categoria;
        p.StockMinimo = cambios.StockMinimo;
        p.PrecioUnitario = cambios.PrecioUnitario;
        await db.SaveChangesAsync();
    }

    /// <summary>Entrada (cantidad positiva) o retiro (negativa). No se retira más de lo que hay.</summary>
    public async Task<string> MoverAsync(int id, int cantidad, string? detalle)
    {
        var p = await BuscarAsync(id);
        if (cantidad == 0) throw new ReglaNegocioException("La cantidad debe ser distinta de cero");
        RegistrarMovimiento(p, cantidad, string.IsNullOrWhiteSpace(detalle) ? (cantidad > 0 ? "Entrada manual" : "Retiro manual") : detalle.Trim());
        await db.SaveChangesAsync();
        return p.EsCritico
            ? $"⚠ {p.Nombre} quedó en stock crítico ({p.Stock} de mínimo {p.StockMinimo}). Se sugiere comprar {p.CantidadSugerida} unidades."
            : $"Movimiento registrado. Stock actual de {p.Nombre}: {p.Stock}.";
    }

    /// <summary>Aplica el movimiento sin guardar (lo usa también la recepción de órdenes de compra).</summary>
    public void RegistrarMovimiento(Producto p, int cantidad, string detalle)
    {
        if (!p.Activo) throw new ReglaNegocioException("El producto está inactivo");
        if (p.Stock + cantidad < 0)
            throw new ReglaNegocioException($"Stock insuficiente: hay {p.Stock} unidades de {p.Nombre} y se intentan retirar {-cantidad}");
        p.Stock += cantidad;
        db.Movimientos.Add(new MovimientoInventario
        {
            ProductoId = p.Id, Producto = p, Tipo = cantidad > 0 ? "ENTRADA" : "SALIDA",
            Cantidad = Math.Abs(cantidad), StockResultante = p.Stock, Detalle = detalle
        });
    }

    /// <summary>Solo se inactiva un producto sin existencias, para no perder inventario sin ajustar.</summary>
    public async Task InactivarAsync(int id)
    {
        var p = await BuscarAsync(id);
        if (p.Stock > 0) throw new ReglaNegocioException("El producto tiene existencias sin ajustar: retírelas antes de inactivarlo");
        p.Activo = false;
        await db.SaveChangesAsync();
    }
}
