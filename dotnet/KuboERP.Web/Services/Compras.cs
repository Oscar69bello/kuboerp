using System.Text.RegularExpressions;
using KuboERP.Web.Data;
using KuboERP.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Services;

/// <summary>Violación de una regla de negocio. El controlador la muestra al usuario como mensaje.</summary>
public class ReglaNegocioException : Exception
{
    public ReglaNegocioException(string mensaje) : base(mensaje) { }
}

// ============================ PROVEEDORES (EP05-US01) ============================

public class ProveedorService
{
    private static readonly Regex Nit = new(@"^\d{9,10}$");
    private static readonly Regex Correo = new(@"^[\w.+-]+@[\w-]+(\.[\w-]+)+$");
    private readonly KuboDbContext db;

    public ProveedorService(KuboDbContext db) => this.db = db;

    public Task<List<Proveedor>> ListarAsync(string? buscar, string? estado) =>
        db.Proveedores
          .Where(p => buscar == null || p.Nombre.Contains(buscar) || p.Nit.Contains(buscar))
          .Where(p => estado == null || p.Estado == estado)
          .OrderBy(p => p.Nombre).ToListAsync();

    public async Task<Proveedor> BuscarAsync(int id) =>
        await db.Proveedores.FindAsync(id) ?? throw new ReglaNegocioException("Proveedor no encontrado");

    public async Task CrearAsync(Proveedor p)
    {
        Validar(p);
        if (await db.Proveedores.AnyAsync(x => x.Nit == p.Nit))
            throw new ReglaNegocioException("El NIT ya está registrado");
        p.Nombre = p.Nombre.Trim();
        p.Estado = EstadosProveedor.Activo;
        db.Proveedores.Add(p);
        await db.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Proveedor cambios)
    {
        Validar(cambios);
        var p = await BuscarAsync(cambios.Id);
        p.Nombre = cambios.Nombre.Trim();
        p.Correo = cambios.Correo;
        p.Telefono = cambios.Telefono;
        p.Presupuesto = cambios.Presupuesto;
        await db.SaveChangesAsync();
    }

    /// <summary>
    /// Un proveedor con órdenes de compra o cotizaciones no se borra: pasa a INACTIVO para conservar el historial.
    /// Devuelve el mensaje para el usuario.
    /// </summary>
    public async Task<string> EliminarAsync(int id)
    {
        var p = await BuscarAsync(id);
        bool tieneHistorial = await db.Ordenes.AnyAsync(o => o.ProveedorId == id)
                              || await db.Cotizaciones.AnyAsync(c => c.ProveedorId == id);
        if (tieneHistorial)
        {
            p.Estado = EstadosProveedor.Inactivo;
            await db.SaveChangesAsync();
            return $"{p.Nombre} tiene órdenes o cotizaciones: no se elimina, queda INACTIVO.";
        }
        db.Proveedores.Remove(p);
        await db.SaveChangesAsync();
        return $"Proveedor {p.Nombre} eliminado.";
    }

    public async Task ReactivarAsync(int id)
    {
        var p = await BuscarAsync(id);
        p.Estado = EstadosProveedor.Activo;
        await db.SaveChangesAsync();
    }

    private static void Validar(Proveedor p)
    {
        if (!Nit.IsMatch(p.Nit ?? "")) throw new ReglaNegocioException("NIT inválido: debe tener 9 o 10 dígitos");
        if (string.IsNullOrWhiteSpace(p.Nombre)) throw new ReglaNegocioException("El nombre es obligatorio");
        if (!Correo.IsMatch(p.Correo ?? "")) throw new ReglaNegocioException("Formato de correo inválido");
        if (p.Presupuesto < 0) throw new ReglaNegocioException("El presupuesto no puede ser negativo");
    }
}

// ============================ COTIZACIONES (EP05-US03, US04) ============================

public class CotizacionService
{
    private readonly KuboDbContext db;
    public CotizacionService(KuboDbContext db) => this.db = db;

    public Task<List<SolicitudCotizacion>> ListarSolicitudesAsync() =>
        db.Solicitudes.Include(s => s.Cotizaciones).ThenInclude(c => c.Proveedor)
          .OrderByDescending(s => s.Fecha).ToListAsync();

    public async Task<SolicitudCotizacion> BuscarSolicitudAsync(int id) =>
        await db.Solicitudes.Include(s => s.Cotizaciones).ThenInclude(c => c.Proveedor)
                .FirstOrDefaultAsync(s => s.Id == id)
        ?? throw new ReglaNegocioException("Solicitud no encontrada");

    public async Task AbrirSolicitudAsync(string codigo, string descripcion)
    {
        if (string.IsNullOrWhiteSpace(codigo)) throw new ReglaNegocioException("El código de la solicitud es obligatorio");
        if (string.IsNullOrWhiteSpace(descripcion)) throw new ReglaNegocioException("La descripción es obligatoria");
        if (await db.Solicitudes.AnyAsync(s => s.Codigo == codigo)) throw new ReglaNegocioException("La solicitud ya existe");
        db.Solicitudes.Add(new SolicitudCotizacion { Codigo = codigo.Trim().ToUpper(), Descripcion = descripcion.Trim() });
        await db.SaveChangesAsync();
    }

    public async Task RegistrarAsync(int solicitudId, int proveedorId, decimal monto, int diasEntrega)
    {
        var s = await BuscarSolicitudAsync(solicitudId);
        if (s.Estado != "ABIERTA") throw new ReglaNegocioException("La solicitud no está abierta");
        if (monto <= 0) throw new ReglaNegocioException("Monto inválido: debe ser mayor que cero");
        var prov = await db.Proveedores.FindAsync(proveedorId);
        if (prov is null || prov.Estado != EstadosProveedor.Activo)
            throw new ReglaNegocioException("El proveedor no existe o está inactivo");
        if (s.Cotizaciones.Any(c => c.ProveedorId == proveedorId))
            throw new ReglaNegocioException("El proveedor ya cotizó esta solicitud");
        int n = await db.Cotizaciones.CountAsync() + 1;
        db.Cotizaciones.Add(new Cotizacion
        {
            Codigo = $"COT-{n:000}", SolicitudId = s.Id, ProveedorId = proveedorId,
            Monto = monto, DiasEntrega = diasEntrega
        });
        await db.SaveChangesAsync();
    }

    /// <summary>Elige la ganadora, rechaza las demás recibidas y cierra la solicitud.</summary>
    public async Task<Cotizacion> SeleccionarAsync(int cotizacionId)
    {
        var ganadora = await BuscarRecibidaAsync(cotizacionId);
        var otras = await db.Cotizaciones
            .Where(c => c.SolicitudId == ganadora.SolicitudId && c.Id != ganadora.Id && c.Estado == "RECIBIDA").ToListAsync();
        otras.ForEach(c => c.Estado = "RECHAZADA");
        ganadora.Estado = "SELECCIONADA";
        ganadora.Solicitud!.Estado = "CERRADA";
        await db.SaveChangesAsync();
        return ganadora;
    }

    public async Task AnularAsync(int cotizacionId)
    {
        var c = await BuscarRecibidaAsync(cotizacionId);
        c.Estado = "ANULADA";
        await db.SaveChangesAsync();
    }

    private async Task<Cotizacion> BuscarRecibidaAsync(int id)
    {
        var c = await db.Cotizaciones.Include(x => x.Solicitud).FirstOrDefaultAsync(x => x.Id == id)
                ?? throw new ReglaNegocioException("Cotización no encontrada");
        if (c.Estado != "RECIBIDA") throw new ReglaNegocioException("Solo se modifican cotizaciones en estado RECIBIDA");
        return c;
    }
}

// ============================ ÓRDENES DE COMPRA (EP05-US05, US06) ============================

public record LineaNueva(int ProductoId, int Cantidad, decimal PrecioUnitario);

public class OrdenCompraService
{
    private readonly KuboDbContext db;
    private readonly InventarioService inventario;

    public OrdenCompraService(KuboDbContext db, InventarioService inventario)
    {
        this.db = db;
        this.inventario = inventario;
    }

    public Task<List<OrdenCompra>> ListarAsync(string? estado) =>
        db.Ordenes.Include(o => o.Proveedor)
          .Where(o => estado == null || o.Estado == estado)
          .OrderByDescending(o => o.Fecha).ToListAsync();

    public async Task<OrdenCompra> BuscarAsync(int id) =>
        await db.Ordenes.Include(o => o.Proveedor)
                .Include(o => o.Lineas).ThenInclude(l => l.Producto)
                .Include(o => o.Auditoria)
                .FirstOrDefaultAsync(o => o.Id == id)
        ?? throw new ReglaNegocioException("Orden no encontrada");

    public async Task<string> SiguienteCodigoAsync() => $"OC-2026-{await db.Ordenes.CountAsync() + 1:000}";

    public async Task<OrdenCompra> CrearAsync(int proveedorId, IEnumerable<LineaNueva> lineas)
    {
        var prov = await db.Proveedores.FindAsync(proveedorId);
        if (prov is null || prov.Estado != EstadosProveedor.Activo)
            throw new ReglaNegocioException("El proveedor no existe o está inactivo");
        var lista = lineas.Where(l => l.ProductoId > 0).ToList();
        if (lista.Count == 0) throw new ReglaNegocioException("La orden debe tener al menos un producto");
        if (lista.Any(l => l.Cantidad <= 0 || l.PrecioUnitario <= 0))
            throw new ReglaNegocioException("Cantidad y precio unitario deben ser mayores que cero");

        var orden = new OrdenCompra
        {
            Codigo = await SiguienteCodigoAsync(),
            ProveedorId = proveedorId,
            Lineas = lista.Select(l => new LineaOrden
                { ProductoId = l.ProductoId, Cantidad = l.Cantidad, PrecioUnitario = l.PrecioUnitario }).ToList()
        };
        orden.Monto = orden.Lineas.Sum(l => l.Subtotal);
        Auditar(orden, "", EstadosOrden.Pendiente, "Orden creada");
        db.Ordenes.Add(orden);
        await db.SaveChangesAsync();
        return orden;
    }

    /// <summary>Aprobar descuenta el monto del presupuesto del proveedor; no se aprueba dos veces.</summary>
    public async Task AprobarAsync(int id)
    {
        var o = await BuscarAsync(id);
        if (o.Estado == EstadosOrden.Aprobada) throw new ReglaNegocioException("La orden ya está aprobada");
        if (o.Estado != EstadosOrden.Pendiente) throw new ReglaNegocioException("Solo se aprueban órdenes pendientes");
        if (o.Monto > o.Proveedor!.Presupuesto)
            throw new ReglaNegocioException(
                $"Presupuesto insuficiente: la orden vale {Formato.Pesos(o.Monto)} y el proveedor tiene {Formato.Pesos(o.Proveedor.Presupuesto)}");
        o.Proveedor.Presupuesto -= o.Monto;
        CambiarEstado(o, EstadosOrden.Aprobada, $"Presupuesto descontado: {Formato.Pesos(o.Monto)}");
        await db.SaveChangesAsync();
    }

    /// <summary>Recibir la mercancía genera la entrada de cada producto en el inventario.</summary>
    public async Task RecibirAsync(int id)
    {
        var o = await BuscarAsync(id);
        if (o.Estado != EstadosOrden.Aprobada) throw new ReglaNegocioException("Solo se reciben órdenes aprobadas");
        foreach (var l in o.Lineas)
            inventario.RegistrarMovimiento(l.Producto!, l.Cantidad, $"Recepción de la orden {o.Codigo}");
        CambiarEstado(o, EstadosOrden.Recibida, "Entrada de inventario generada");
        await db.SaveChangesAsync();
    }

    /// <summary>Cancelar exige justificación; si estaba aprobada, devuelve el monto al presupuesto.</summary>
    public async Task CancelarAsync(int id, string? justificacion)
    {
        var o = await BuscarAsync(id);
        if (!EstadosOrden.Activos.Contains(o.Estado))
            throw new ReglaNegocioException("Solo se cancelan órdenes pendientes o aprobadas");
        if (string.IsNullOrWhiteSpace(justificacion))
            throw new ReglaNegocioException("La cancelación exige una justificación");
        if (o.Estado == EstadosOrden.Aprobada) o.Proveedor!.Presupuesto += o.Monto;
        o.Justificacion = justificacion.Trim();
        CambiarEstado(o, EstadosOrden.Cancelada, o.Justificacion);
        await db.SaveChangesAsync();
    }

    private static void CambiarEstado(OrdenCompra o, string nuevo, string detalle)
    {
        Auditar(o, o.Estado, nuevo, detalle);
        o.Estado = nuevo;
    }

    private static void Auditar(OrdenCompra o, string anterior, string nuevo, string detalle) =>
        o.Auditoria.Add(new AuditoriaOrden { EstadoAnterior = anterior, EstadoNuevo = nuevo, Detalle = detalle });
}
