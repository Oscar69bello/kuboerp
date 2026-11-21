using KuboERP.Web.Data;
using KuboERP.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace KuboERP.Web.Services;

// ============================ EMPLEADOS (EP06-US01 a US03) ============================

public class EmpleadoService
{
    private readonly KuboDbContext db;
    public EmpleadoService(KuboDbContext db) => this.db = db;

    public Task<List<Empleado>> ListarAsync(string? cargo, string estado = "ACTIVO") =>
        db.Empleados.Where(e => cargo == null || e.Cargo == cargo)
          .Where(e => estado == "TODOS" || e.Estado == estado)
          .OrderBy(e => e.Nombre).ToListAsync();

    public async Task<Empleado> BuscarAsync(int id) =>
        await db.Empleados.FindAsync(id) ?? throw new ReglaNegocioException("Empleado no encontrado");

    public async Task CrearAsync(Empleado e)
    {
        Validar(e);
        if (await db.Empleados.AnyAsync(x => x.Cedula == e.Cedula))
            throw new ReglaNegocioException("La cédula ya está registrada");
        e.Nombre = e.Nombre.Trim();
        e.Estado = "ACTIVO";
        db.Empleados.Add(e);
        await db.SaveChangesAsync();
    }

    public async Task ActualizarAsync(Empleado cambios)
    {
        Validar(cambios);
        var e = await BuscarAsync(cambios.Id);
        e.Nombre = cambios.Nombre.Trim();
        e.Cargo = cambios.Cargo;
        e.TipoContrato = cambios.TipoContrato;
        e.SalarioBase = cambios.SalarioBase;
        await db.SaveChangesAsync();
    }

    public async Task DesvincularAsync(int id)
    {
        var e = await BuscarAsync(id);
        if (e.Estado == "RETIRADO") throw new ReglaNegocioException("El empleado ya está desvinculado");
        e.Estado = "RETIRADO";
        await db.SaveChangesAsync();
    }

    private static void Validar(Empleado e)
    {
        if (string.IsNullOrWhiteSpace(e.Nombre)) throw new ReglaNegocioException("El nombre es obligatorio");
        if (!Cargos.Todos.Contains(e.Cargo)) throw new ReglaNegocioException("Cargo inválido");
        if (!Cargos.Contratos.Contains(e.TipoContrato)) throw new ReglaNegocioException("Tipo de contrato inválido");
        if (e.SalarioBase < ParametrosNomina.Smmlv)
            throw new ReglaNegocioException($"El salario no puede ser inferior al salario mínimo ({Formato.Pesos(ParametrosNomina.Smmlv)})");
    }
}

// ============================ NÓMINA (EP06-US04) ============================

/// <summary>Parámetros legales 2026. Se actualizan cada año sin tocar el motor (SOLID · O).</summary>
public static class ParametrosNomina
{
    public const decimal Smmlv = 1_750_905m;              // Decreto 1469 de 2025
    public const decimal AuxilioTransporte = 249_095m;    // Decreto 1470 de 2025
    public const decimal HorasMensuales = 180m;           // 42 h semanales desde el 15 de julio de 2026 (Ley 2101 de 2021)
    public const decimal RecargoExtraDiurna = 0.25m;
    public const decimal ComisionVentas = 0.02m;
    public const decimal SaludTrabajador = 0.04m, PensionTrabajador = 0.04m, SolidaridadPensional = 0.01m;
    public const decimal PensionEmpleador = 0.12m, SaludEmpleador = 0.085m, CajaCompensacion = 0.04m;
    public const decimal Sena = 0.02m, Icbf = 0.03m, LimiteNoSalarial = 0.40m;

    public static decimal TarifaArl(int clase) => clase switch
    {
        1 => 0.00522m, 2 => 0.01044m, 3 => 0.02436m, 4 => 0.0435m, _ => 0.0696m
    };
}

public class NovedadNomina
{
    public int EmpleadoId { get; set; }
    public int DiasLaborados { get; set; } = 30;
    public int HorasExtra { get; set; }
    public decimal Ventas { get; set; }
    public decimal Bonificacion { get; set; }
}

public class NominaService
{
    private readonly KuboDbContext db;
    public NominaService(KuboDbContext db) => this.db = db;

    public Task<List<string>> PeriodosAsync() =>
        db.Desprendibles.Select(d => d.Periodo).Distinct().OrderByDescending(p => p).ToListAsync();

    public Task<List<DesprendibleNomina>> DesprendiblesAsync(string periodo) =>
        db.Desprendibles.Include(d => d.Empleado).Where(d => d.Periodo == periodo)
          .OrderBy(d => d.Empleado!.Nombre).ToListAsync();

    public async Task<DesprendibleNomina> DesprendibleAsync(int id) =>
        await db.Desprendibles.Include(d => d.Empleado).FirstOrDefaultAsync(d => d.Id == id)
        ?? throw new ReglaNegocioException("Desprendible no encontrado");

    /// <summary>Liquida el periodo para todos los empleados activos y reemplaza la liquidación anterior del mismo periodo.</summary>
    public async Task<int> LiquidarAsync(string periodo, IEnumerable<NovedadNomina> novedades)
    {
        if (!System.Text.RegularExpressions.Regex.IsMatch(periodo ?? "", @"^\d{4}-\d{2}$"))
            throw new ReglaNegocioException("Periodo inválido: use el formato AAAA-MM");
        var porEmpleado = novedades.ToDictionary(n => n.EmpleadoId);
        if (porEmpleado.Values.Any(n => n.DiasLaborados is < 0 or > 30))
            throw new ReglaNegocioException("Los días laborados deben estar entre 0 y 30");
        if (porEmpleado.Values.Any(n => n.HorasExtra < 0 || n.Ventas < 0 || n.Bonificacion < 0))
            throw new ReglaNegocioException("Las novedades no pueden ser negativas");

        var anteriores = db.Desprendibles.Where(d => d.Periodo == periodo);
        db.Desprendibles.RemoveRange(anteriores);

        var activos = await db.Empleados.Where(e => e.Estado == "ACTIVO").ToListAsync();
        foreach (var e in activos)
        {
            var d = Calcular(e, porEmpleado.GetValueOrDefault(e.Id) ?? new NovedadNomina { EmpleadoId = e.Id });
            d.Periodo = periodo!;
            db.Desprendibles.Add(d);
        }
        await db.SaveChangesAsync();
        return activos.Count;
    }

    /// <summary>Motor de nómina con la normativa colombiana 2026 (mismas reglas que el motor en Python).</summary>
    public static DesprendibleNomina Calcular(Empleado e, NovedadNomina n)
    {
        decimal dias = n.DiasLaborados;
        decimal proporcional = e.SalarioBase * dias / 30;

        decimal salarial = e.Cargo switch
        {
            Cargos.Tecnico => proporcional + n.HorasExtra * (e.SalarioBase / ParametrosNomina.HorasMensuales) * (1 + ParametrosNomina.RecargoExtraDiurna),
            Cargos.Vendedor => proporcional + n.Ventas * ParametrosNomina.ComisionVentas,
            _ => proporcional
        };
        decimal noSalarial = e.Cargo == Cargos.Gerente ? n.Bonificacion : 0;

        // Auxilio de transporte para quien devenga hasta 2 SMMLV (Ley 15 de 1959), proporcional a los días
        decimal auxilio = e.SalarioBase <= 2 * ParametrosNomina.Smmlv ? ParametrosNomina.AuxilioTransporte * dias / 30 : 0;

        // IBC: el exceso no salarial sobre el 40 % suma (Ley 1393 de 2010) y nunca es menor que un SMMLV proporcional
        decimal exceso = Math.Max(0, noSalarial - ParametrosNomina.LimiteNoSalarial * (salarial + noSalarial));
        decimal ibc = Math.Max(salarial + exceso, ParametrosNomina.Smmlv * dias / 30);

        decimal fsp = ibc >= 4 * ParametrosNomina.Smmlv ? ibc * ParametrosNomina.SolidaridadPensional : 0;

        decimal aportes = ibc * ParametrosNomina.PensionEmpleador
                        + ibc * ParametrosNomina.TarifaArl(e.NivelRiesgoArl)
                        + ibc * ParametrosNomina.CajaCompensacion;
        // Salud, SENA e ICBF del empleador solo desde 10 SMMLV (exoneración, art. 114-1 del Estatuto Tributario)
        if (salarial >= 10 * ParametrosNomina.Smmlv)
            aportes += ibc * (ParametrosNomina.SaludEmpleador + ParametrosNomina.Sena + ParametrosNomina.Icbf);

        return new DesprendibleNomina
        {
            EmpleadoId = e.Id, Empleado = e,
            DiasLaborados = n.DiasLaborados, HorasExtra = n.HorasExtra, Ventas = n.Ventas, Bonificacion = n.Bonificacion,
            DevengadoSalarial = Math.Round(salarial), AuxilioTransporte = Math.Round(auxilio),
            DevengadoNoSalarial = Math.Round(noSalarial), Ibc = Math.Round(ibc),
            Salud = Math.Round(ibc * ParametrosNomina.SaludTrabajador),
            Pension = Math.Round(ibc * ParametrosNomina.PensionTrabajador),
            SolidaridadPensional = Math.Round(fsp),
            AportesEmpleador = Math.Round(aportes)
        };
    }
}

public static class Formato
{
    private static readonly System.Globalization.CultureInfo Co = new("es-CO");
    public static string Pesos(decimal v) => "$ " + v.ToString("N0", Co);
    public static string Numero(decimal v) => v.ToString("N0", Co);
}
