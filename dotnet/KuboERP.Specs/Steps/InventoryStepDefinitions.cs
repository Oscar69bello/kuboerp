using FluentAssertions;
using KuboERP.Specs.Inventario;
using Reqnroll; // En un proyecto heredado con SpecFlow: using TechTalk.SpecFlow;

namespace KuboERP.Specs.Steps;

[Binding]
public class InventoryStepDefinitions
{
    private readonly InventoryService _service = new(new InMemoryProductRepository());
    private Product? _producto;
    private Exception? _excepcion;
    private string _codigo = "";

    [Given(@"que no existe un producto con código ""(.*)""")]
    public void DadoQueNoExisteProducto(string codigo)
    {
        _service.ExistsByCode(codigo).Should().BeFalse();
    }

    [When(@"registro el producto con código ""(.*)"" y stock inicial (.*)")]
    public void CuandoRegistroProducto(string codigo, int stock)
    {
        try
        {
            _producto = _service.Register(new Product(codigo, stock));
        }
        catch (Exception e) { _excepcion = e; }
    }

    [Then(@"el producto se crea con estado ""(.*)""")]
    public void EntoncesProductoSeCreaConEstado(string estado)
    {
        _producto.Should().NotBeNull();
        _producto!.Estado.Should().Be(estado);
    }

    // ---- Ejercicio 5: retiro mayor al stock disponible ----

    [Given(@"que el producto ""(.*)"" tiene stock (\d+)")]
    public void DadoQueElProductoTieneStock(string codigo, int stock)
    {
        _codigo = codigo;
        _service.Register(new Product(codigo, stock));
    }

    [When(@"intento retirar (\d+) unidades")]
    public void CuandoIntentoRetirar(int cantidad)
    {
        try
        {
            _service.Withdraw(_codigo, cantidad);
        }
        catch (Exception e) { _excepcion = e; }
    }

    [Then(@"se lanza InsufficientStockException")]
    public void EntoncesSeLanzaInsufficientStockException()
    {
        _excepcion.Should().BeOfType<InsufficientStockException>()
            .Which.Message.Should().Be("Stock insuficiente");
    }

    [Then(@"el stock permanece en (\d+)")]
    public void EntoncesElStockPermaneceEn(int esperado)
    {
        _service.StockOf(_codigo).Should().Be(esperado);
    }

    [Then(@"el stock queda en (\d+)")]
    public void EntoncesElStockQuedaEn(int esperado)
    {
        _excepcion.Should().BeNull();
        _service.StockOf(_codigo).Should().Be(esperado);
    }
}
