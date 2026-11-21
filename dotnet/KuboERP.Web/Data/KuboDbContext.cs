using KuboERP.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Data;

public class KuboDbContext : DbContext
{
    public KuboDbContext(DbContextOptions<KuboDbContext> options) : base(options) { }

    public DbSet<Proveedor> Proveedores => Set<Proveedor>();
    public DbSet<SolicitudCotizacion> Solicitudes => Set<SolicitudCotizacion>();
    public DbSet<Cotizacion> Cotizaciones => Set<Cotizacion>();
    public DbSet<OrdenCompra> Ordenes => Set<OrdenCompra>();
    public DbSet<LineaOrden> LineasOrden => Set<LineaOrden>();
    public DbSet<AuditoriaOrden> AuditoriaOrdenes => Set<AuditoriaOrden>();
    public DbSet<Producto> Productos => Set<Producto>();
    public DbSet<MovimientoInventario> Movimientos => Set<MovimientoInventario>();
    public DbSet<Empleado> Empleados => Set<Empleado>();
    public DbSet<DesprendibleNomina> Desprendibles => Set<DesprendibleNomina>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        // Reglas de unicidad que también garantiza la base de datos
        b.Entity<Proveedor>().HasIndex(p => p.Nit).IsUnique();
        b.Entity<Producto>().HasIndex(p => p.Codigo).IsUnique();
        b.Entity<Empleado>().HasIndex(e => e.Cedula).IsUnique();
        b.Entity<OrdenCompra>().HasIndex(o => o.Codigo).IsUnique();
        b.Entity<SolicitudCotizacion>().HasIndex(s => s.Codigo).IsUnique();
        b.Entity<Cotizacion>().HasIndex(c => c.Codigo).IsUnique();
        b.Entity<Cotizacion>().HasIndex(c => new { c.SolicitudId, c.ProveedorId }).IsUnique();
        b.Entity<DesprendibleNomina>().HasIndex(d => new { d.Periodo, d.EmpleadoId }).IsUnique();

        // Sin borrados en cascada: el historial de compras y de nómina se conserva
        foreach (var fk in b.Model.GetEntityTypes().SelectMany(t => t.GetForeignKeys()))
            fk.DeleteBehavior = DeleteBehavior.Restrict;

        b.Entity<LineaOrden>().HasOne<OrdenCompra>().WithMany(o => o.Lineas)
            .HasForeignKey(l => l.OrdenCompraId).OnDelete(DeleteBehavior.Cascade);
        b.Entity<AuditoriaOrden>().HasOne<OrdenCompra>().WithMany(o => o.Auditoria)
            .HasForeignKey(a => a.OrdenCompraId).OnDelete(DeleteBehavior.Cascade);
    }
}
