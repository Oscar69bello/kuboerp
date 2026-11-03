namespace KuboERP.Specs.Inventario;

/// <summary>Producto, materia prima o insumo eléctrico del inventario de KuboERP.</summary>
public class Product
{
    public Product(string codigo, int stock)
    {
        Codigo = codigo;
        Stock = stock;
    }

    public string Codigo { get; }
    public int Stock { get; set; }
    public string Estado { get; set; } = "DISPONIBLE";
}

public class InsufficientStockException : Exception
{
    public InsufficientStockException(string mensaje) : base(mensaje) { }
}

public class InMemoryProductRepository
{
    private readonly Dictionary<string, Product> _datos = new();

    public bool Exists(string codigo) => _datos.ContainsKey(codigo);
    public Product? Find(string codigo) => _datos.GetValueOrDefault(codigo);
    public Product Save(Product producto) => _datos[producto.Codigo] = producto;
}

/// <summary>Registro y retiro de inventario (Ejercicio 5 · SpecFlow/Reqnroll).</summary>
public class InventoryService
{
    private readonly InMemoryProductRepository _repositorio;

    public InventoryService(InMemoryProductRepository repositorio) => _repositorio = repositorio;

    public bool ExistsByCode(string codigo) => _repositorio.Exists(codigo);

    public Product Register(Product producto)
    {
        if (_repositorio.Exists(producto.Codigo))
            throw new InvalidOperationException("El código ya está registrado");
        if (producto.Stock < 0)
            throw new InvalidOperationException("El stock inicial no puede ser negativo");
        producto.Estado = "DISPONIBLE";
        return _repositorio.Save(producto);
    }

    public int Withdraw(string codigo, int cantidad)
    {
        var producto = _repositorio.Find(codigo)
                       ?? throw new InvalidOperationException("Producto no encontrado");
        if (cantidad > producto.Stock)
            throw new InsufficientStockException("Stock insuficiente");
        producto.Stock -= cantidad;
        return producto.Stock;
    }

    public int StockOf(string codigo) => _repositorio.Find(codigo)!.Stock;
}
