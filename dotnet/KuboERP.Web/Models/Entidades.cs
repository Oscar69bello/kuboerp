using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace KuboERP.Web.Models;

// ============================ COMPRAS ============================

public class Proveedor
{
    public int Id { get; set; }

    [Required(ErrorMessage = "El NIT es obligatorio")]
    [RegularExpression(@"^\d{9,10}$", ErrorMessage = "El NIT debe tener 9 o 10 dígitos, sin puntos ni guion")]
    [StringLength(10)]
    public string Nit { get; set; } = "";

    [Required(ErrorMessage = "El nombre es obligatorio")]
    [StringLength(120)]
    public string Nombre { get; set; } = "";

    [Required(ErrorMessage = "El correo es obligatorio")]
    [EmailAddress(ErrorMessage = "Formato de correo inválido")]
    [StringLength(120)]
    public string Correo { get; set; } = "";

    [StringLength(20)]
    public string? Telefono { get; set; }

    [Range(0, 9_999_999_999, ErrorMessage = "El presupuesto no puede ser negativo")]
    [Column(TypeName = "decimal(18,0)")]
    public decimal Presupuesto { get; set; }

    [StringLength(10)]
    public string Estado { get; set; } = EstadosProveedor.Activo;

    public List<OrdenCompra> Ordenes { get; set; } = new();
}

public static class EstadosProveedor
{
    public const string Activo = "ACTIVO";
    public const string Inactivo = "INACTIVO";
}

public class SolicitudCotizacion
{
    public int Id { get; set; }

    [Required(ErrorMessage = "El código es obligatorio")]
    [StringLength(20)]
    public string Codigo { get; set; } = "";

    [Required(ErrorMessage = "La descripción es obligatoria")]
    [StringLength(200)]
    public string Descripcion { get; set; } = "";

    public DateTime Fecha { get; set; } = DateTime.Now;

    [StringLength(10)]
    public string Estado { get; set; } = "ABIERTA";

    public List<Cotizacion> Cotizaciones { get; set; } = new();
}

public class Cotizacion
{
    public int Id { get; set; }

    [Required, StringLength(20)]
    public string Codigo { get; set; } = "";

    public int SolicitudId { get; set; }
    public SolicitudCotizacion? Solicitud { get; set; }

    public int ProveedorId { get; set; }
    public Proveedor? Proveedor { get; set; }

    [Column(TypeName = "decimal(18,0)")]
    public decimal Monto { get; set; }

    public int DiasEntrega { get; set; }

    public DateTime Fecha { get; set; } = DateTime.Now;

    /// <summary>RECIBIDA, SELECCIONADA, RECHAZADA o ANULADA.</summary>
    [StringLength(12)]
    public string Estado { get; set; } = "RECIBIDA";
}

public class OrdenCompra
{
    public int Id { get; set; }

    [Required, StringLength(20)]
    public string Codigo { get; set; } = "";

    public int ProveedorId { get; set; }
    public Proveedor? Proveedor { get; set; }

    public DateTime Fecha { get; set; } = DateTime.Now;

    [Column(TypeName = "decimal(18,0)")]
    public decimal Monto { get; set; }

    /// <summary>PENDIENTE → APROBADA → RECIBIDA; PENDIENTE | APROBADA → CANCELADA.</summary>
    [StringLength(10)]
    public string Estado { get; set; } = EstadosOrden.Pendiente;

    [StringLength(300)]
    public string? Justificacion { get; set; }

    public List<LineaOrden> Lineas { get; set; } = new();
    public List<AuditoriaOrden> Auditoria { get; set; } = new();
}

public static class EstadosOrden
{
    public const string Pendiente = "PENDIENTE";
    public const string Aprobada = "APROBADA";
    public const string Recibida = "RECIBIDA";
    public const string Cancelada = "CANCELADA";
    public static readonly string[] Activos = { Pendiente, Aprobada };
}

public class LineaOrden
{
    public int Id { get; set; }
    public int OrdenCompraId { get; set; }
    public int ProductoId { get; set; }
    public Producto? Producto { get; set; }
    public int Cantidad { get; set; }

    [Column(TypeName = "decimal(18,0)")]
    public decimal PrecioUnitario { get; set; }

    [NotMapped]
    public decimal Subtotal => Cantidad * PrecioUnitario;
}

public class AuditoriaOrden
{
    public int Id { get; set; }
    public int OrdenCompraId { get; set; }
    public DateTime Fecha { get; set; } = DateTime.Now;
    [StringLength(10)] public string EstadoAnterior { get; set; } = "";
    [StringLength(10)] public string EstadoNuevo { get; set; } = "";
    [StringLength(300)] public string Detalle { get; set; } = "";
}

// ============================ INVENTARIO ============================

public class Producto
{
    public int Id { get; set; }

    [Required(ErrorMessage = "El código es obligatorio")]
    [StringLength(20)]
    public string Codigo { get; set; } = "";

    [Required(ErrorMessage = "El nombre es obligatorio")]
    [StringLength(120)]
    public string Nombre { get; set; } = "";

    [Required(ErrorMessage = "La categoría es obligatoria")]
    [StringLength(40)]
    public string Categoria { get; set; } = "";

    [Range(0, int.MaxValue, ErrorMessage = "El stock no puede ser negativo")]
    public int Stock { get; set; }

    [Display(Name = "Stock mínimo")]
    [Range(0, int.MaxValue, ErrorMessage = "El stock mínimo no puede ser negativo")]
    public int StockMinimo { get; set; }

    [Display(Name = "Precio unitario")]
    [Range(0, 999_999_999, ErrorMessage = "El precio no puede ser negativo")]
    [Column(TypeName = "decimal(18,0)")]
    public decimal PrecioUnitario { get; set; }

    public bool Activo { get; set; } = true;

    /// <summary>Stock crítico: hay un mínimo definido y el stock llegó a él o está por debajo.</summary>
    [NotMapped]
    public bool EsCritico => StockMinimo > 0 && Stock <= StockMinimo;

    /// <summary>Cantidad sugerida para reponer hasta el doble del mínimo.</summary>
    [NotMapped]
    public int CantidadSugerida => Math.Max(0, StockMinimo * 2 - Stock);
}

public class MovimientoInventario
{
    public int Id { get; set; }
    public int ProductoId { get; set; }
    public Producto? Producto { get; set; }
    public DateTime Fecha { get; set; } = DateTime.Now;

    /// <summary>ENTRADA o SALIDA.</summary>
    [StringLength(8)]
    public string Tipo { get; set; } = "ENTRADA";

    public int Cantidad { get; set; }
    public int StockResultante { get; set; }

    [StringLength(200)]
    public string Detalle { get; set; } = "";
}

// ============================ TALENTO HUMANO ============================

public class Empleado
{
    public int Id { get; set; }

    [Required(ErrorMessage = "La cédula es obligatoria")]
    [RegularExpression(@"^\d{6,10}$", ErrorMessage = "La cédula debe tener entre 6 y 10 dígitos")]
    [StringLength(10)]
    public string Cedula { get; set; } = "";

    [Required(ErrorMessage = "El nombre es obligatorio")]
    [StringLength(120)]
    public string Nombre { get; set; } = "";

    /// <summary>TECNICO, VENDEDOR, GERENTE o ADMINISTRATIVO.</summary>
    [Required(ErrorMessage = "El cargo es obligatorio")]
    [StringLength(15)]
    public string Cargo { get; set; } = Cargos.Tecnico;

    [Display(Name = "Tipo de contrato")]
    [Required, StringLength(15)]
    public string TipoContrato { get; set; } = "INDEFINIDO";

    [Display(Name = "Salario base")]
    [Column(TypeName = "decimal(18,0)")]
    public decimal SalarioBase { get; set; }

    [Display(Name = "Fecha de ingreso")]
    [DataType(DataType.Date)]
    public DateTime FechaIngreso { get; set; } = DateTime.Today;

    [StringLength(10)]
    public string Estado { get; set; } = "ACTIVO";

    /// <summary>Clase de riesgo ARL (Decreto 1295 de 1994): el técnico de campo es clase 4.</summary>
    [NotMapped]
    public int NivelRiesgoArl => Cargo == Cargos.Tecnico ? 4 : 1;
}

public static class Cargos
{
    public const string Tecnico = "TECNICO";
    public const string Vendedor = "VENDEDOR";
    public const string Gerente = "GERENTE";
    public const string Administrativo = "ADMINISTRATIVO";
    public static readonly string[] Todos = { Tecnico, Vendedor, Gerente, Administrativo };
    public static readonly string[] Contratos = { "INDEFINIDO", "FIJO", "OBRA_LABOR" };

    public static string Nombre(string cargo) => cargo switch
    {
        Tecnico => "Técnico electricista",
        Vendedor => "Asesor comercial",
        Gerente => "Gerente",
        _ => "Administrativo"
    };
}

/// <summary>Desprendible de nómina liquidado y guardado para un periodo (AAAA-MM).</summary>
public class DesprendibleNomina
{
    public int Id { get; set; }

    [StringLength(7)]
    public string Periodo { get; set; } = "";

    public int EmpleadoId { get; set; }
    public Empleado? Empleado { get; set; }

    public int DiasLaborados { get; set; }
    public int HorasExtra { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal Ventas { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal Bonificacion { get; set; }

    [Column(TypeName = "decimal(18,0)")] public decimal DevengadoSalarial { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal AuxilioTransporte { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal DevengadoNoSalarial { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal Ibc { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal Salud { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal Pension { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal SolidaridadPensional { get; set; }
    [Column(TypeName = "decimal(18,0)")] public decimal AportesEmpleador { get; set; }

    public DateTime FechaLiquidacion { get; set; } = DateTime.Now;

    [NotMapped] public decimal TotalDevengado => DevengadoSalarial + AuxilioTransporte + DevengadoNoSalarial;
    [NotMapped] public decimal TotalDeducciones => Salud + Pension + SolidaridadPensional;
    [NotMapped] public decimal Neto => TotalDevengado - TotalDeducciones;
    [NotMapped] public decimal CostoEmpleador => TotalDevengado + AportesEmpleador;
}
