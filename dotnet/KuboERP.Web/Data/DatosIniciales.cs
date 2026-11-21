using KuboERP.Web.Models;
using KuboERP.Web.Services;

namespace KuboERP.Web.Data;

/// <summary>Datos de ejemplo de ElectroSoluciones S.A.S. para la primera ejecución.</summary>
public static class DatosIniciales
{
    public static void Cargar(KuboDbContext db)
    {
        if (db.Proveedores.Any()) return;

        // ---------- Proveedores ----------
        var p1 = new Proveedor { Nit = "900123456", Nombre = "Eléctricos del Centro S.A.S.", Correo = "ventas@electricosdelcentro.co", Telefono = "601 345 6789", Presupuesto = 18_500_000 };
        var p2 = new Proveedor { Nit = "800456789", Nombre = "Distribuidora Cables Andinos", Correo = "pedidos@cablesandinos.com", Telefono = "604 222 1010", Presupuesto = 12_000_000 };
        var p3 = new Proveedor { Nit = "901234567", Nombre = "Iluminación LED Colombia", Correo = "comercial@ledcolombia.co", Telefono = "602 555 4433", Presupuesto = 9_800_000 };
        var p4 = new Proveedor { Nit = "860987654", Nombre = "Protecciones Industriales Ltda.", Correo = "contacto@protecind.com", Telefono = "601 777 8899", Presupuesto = 2_500_000 };
        var p5 = new Proveedor { Nit = "830111222", Nombre = "Ferretería La Sabana", Correo = "info@ferresabana.co", Telefono = "601 863 2020", Presupuesto = 4_000_000, Estado = EstadosProveedor.Inactivo };
        db.Proveedores.AddRange(p1, p2, p3, p4, p5);

        // ---------- Productos ----------
        Producto P(string cod, string nom, string cat, int stock, int min, decimal precio) =>
            new() { Codigo = cod, Nombre = nom, Categoria = cat, Stock = stock, StockMinimo = min, PrecioUnitario = precio };
        var cable12 = P("CAB-THHN-12", "Cable THHN calibre 12 AWG (rollo 100 m)", "Cableado", 18, 10, 285_000);
        var cable10 = P("CAB-THHN-10", "Cable THHN calibre 10 AWG (rollo 100 m)", "Cableado", 6, 8, 420_000);
        var brk20 = P("BRK-1X20", "Breaker monopolar 1x20 A", "Protección", 45, 20, 18_500);
        var brk30 = P("BRK-2X30", "Breaker bipolar 2x30 A", "Protección", 2, 10, 52_000);
        var dif = P("DIF-2X40", "Interruptor diferencial 2x40 A", "Protección", 7, 5, 168_000);
        var led = P("LED-PAN-18", "Panel LED 18 W luz blanca", "Iluminación", 64, 25, 34_900);
        var refl = P("LED-REF-100", "Reflector LED 100 W exterior", "Iluminación", 4, 6, 89_000);
        var tab = P("TAB-12C", "Tablero de distribución 12 circuitos", "Tableros", 9, 4, 245_000);
        var pinza = P("HER-PINZA-VA", "Pinza voltiamperimétrica digital", "Herramientas", 5, 2, 320_000);
        var tubo = P("TUB-EMT-34", "Tubo EMT 3/4\" x 3 m", "Tubería y accesorios", 120, 40, 21_000);
        db.Productos.AddRange(cable12, cable10, brk20, brk30, dif, led, refl, tab, pinza, tubo);

        var nov = new DateTime(2026, 11, 3, 8, 0, 0);
        foreach (var p in new[] { cable12, cable10, brk20, brk30, dif, led, refl, tab, pinza, tubo })
            db.Movimientos.Add(new MovimientoInventario { Producto = p, Fecha = nov, Tipo = "ENTRADA", Cantidad = p.Stock, StockResultante = p.Stock, Detalle = "Inventario inicial" });

        // ---------- Cotizaciones ----------
        var s1 = new SolicitudCotizacion { Codigo = "SOL-2026-001", Descripcion = "Cableado para obra residencial Conjunto Los Robles", Fecha = nov.AddDays(1), Estado = "CERRADA" };
        var s2 = new SolicitudCotizacion { Codigo = "SOL-2026-002", Descripcion = "Reposición de breakers y diferenciales", Fecha = nov.AddDays(12), Estado = "ABIERTA" };
        db.Solicitudes.AddRange(s1, s2);
        db.Cotizaciones.AddRange(
            new Cotizacion { Codigo = "COT-001", Solicitud = s1, Proveedor = p2, Monto = 3_980_000, DiasEntrega = 5, Fecha = nov.AddDays(2), Estado = "SELECCIONADA" },
            new Cotizacion { Codigo = "COT-002", Solicitud = s1, Proveedor = p1, Monto = 4_250_000, DiasEntrega = 3, Fecha = nov.AddDays(2), Estado = "RECHAZADA" },
            new Cotizacion { Codigo = "COT-003", Solicitud = s2, Proveedor = p4, Monto = 1_420_000, DiasEntrega = 4, Fecha = nov.AddDays(13) },
            new Cotizacion { Codigo = "COT-004", Solicitud = s2, Proveedor = p1, Monto = 1_310_000, DiasEntrega = 6, Fecha = nov.AddDays(14) });

        // ---------- Órdenes de compra ----------
        OrdenCompra O(string cod, Proveedor prov, DateTime f, string estado, params (Producto p, int c, decimal pu)[] lineas)
        {
            var o = new OrdenCompra { Codigo = cod, Proveedor = prov, Fecha = f, Estado = estado };
            o.Lineas = lineas.Select(l => new LineaOrden { Producto = l.p, Cantidad = l.c, PrecioUnitario = l.pu }).ToList();
            o.Monto = o.Lineas.Sum(l => l.Subtotal);
            o.Auditoria.Add(new AuditoriaOrden { Fecha = f, EstadoAnterior = "", EstadoNuevo = "PENDIENTE", Detalle = "Orden creada" });
            if (estado is "APROBADA" or "RECIBIDA")
                o.Auditoria.Add(new AuditoriaOrden { Fecha = f.AddHours(3), EstadoAnterior = "PENDIENTE", EstadoNuevo = "APROBADA", Detalle = $"Presupuesto descontado: {Formato.Pesos(o.Monto)}" });
            if (estado == "RECIBIDA")
                o.Auditoria.Add(new AuditoriaOrden { Fecha = f.AddDays(4), EstadoAnterior = "APROBADA", EstadoNuevo = "RECIBIDA", Detalle = "Entrada de inventario generada" });
            return o;
        }
        db.Ordenes.AddRange(
            O("OC-2026-001", p2, nov.AddDays(3), "RECIBIDA", (cable12, 10, 270_000), (cable10, 2, 395_000)),
            O("OC-2026-002", p3, nov.AddDays(8), "APROBADA", (led, 40, 31_500), (refl, 6, 84_000)),
            O("OC-2026-003", p1, nov.AddDays(15), "PENDIENTE", (tab, 4, 238_000), (tubo, 50, 19_800)),
            O("OC-2026-004", p4, nov.AddDays(16), "PENDIENTE", (dif, 10, 162_000), (brk30, 20, 49_500)));

        // ---------- Empleados ----------
        var empleados = new[]
        {
            new Empleado { Cedula = "1070945321", Nombre = "Laura Camila Rincón", Cargo = Cargos.Gerente, TipoContrato = "INDEFINIDO", SalarioBase = 19_500_000, FechaIngreso = new(2021, 2, 1) },
            new Empleado { Cedula = "80234567", Nombre = "Jorge Andrés Peña", Cargo = Cargos.Tecnico, TipoContrato = "INDEFINIDO", SalarioBase = 2_600_000, FechaIngreso = new(2022, 6, 13) },
            new Empleado { Cedula = "1019087654", Nombre = "Diego Alejandro Mora", Cargo = Cargos.Tecnico, TipoContrato = "OBRA_LABOR", SalarioBase = 2_100_000, FechaIngreso = new(2025, 3, 3) },
            new Empleado { Cedula = "52876543", Nombre = "Paola Andrea Ruiz", Cargo = Cargos.Vendedor, TipoContrato = "INDEFINIDO", SalarioBase = 1_950_000, FechaIngreso = new(2023, 9, 18) },
            new Empleado { Cedula = "1032456789", Nombre = "Santiago Gómez Ortiz", Cargo = Cargos.Vendedor, TipoContrato = "FIJO", SalarioBase = 1_750_905, FechaIngreso = new(2026, 1, 15) },
            new Empleado { Cedula = "39765432", Nombre = "Marta Lucía Herrera", Cargo = Cargos.Administrativo, TipoContrato = "INDEFINIDO", SalarioBase = 3_400_000, FechaIngreso = new(2020, 8, 10) },
        };
        db.Empleados.AddRange(empleados);
        db.SaveChanges();

        // ---------- Nómina de octubre ya liquidada ----------
        var novedades = new Dictionary<string, NovedadNomina>
        {
            ["1070945321"] = new() { Bonificacion = 4_000_000 },
            ["80234567"] = new() { HorasExtra = 12 },
            ["1019087654"] = new() { HorasExtra = 6, DiasLaborados = 28 },
            ["52876543"] = new() { Ventas = 38_000_000 },
            ["1032456789"] = new() { Ventas = 21_500_000 },
        };
        foreach (var e in empleados)
        {
            var n = novedades.GetValueOrDefault(e.Cedula) ?? new NovedadNomina();
            n.EmpleadoId = e.Id;
            var d = NominaService.Calcular(e, n);
            d.Periodo = "2026-10";
            d.FechaLiquidacion = new DateTime(2026, 10, 30, 17, 0, 0);
            db.Desprendibles.Add(d);
        }
        db.SaveChanges();
    }
}
