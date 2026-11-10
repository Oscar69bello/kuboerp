"""Sprint 2 · Los adaptadores en memoria cumplen los contratos de repositorios.py (SOLID · L y D).

Si mañana se escribe el adaptador de Azure SQL, basta con agregarlo a esta lista: si cumple el contrato,
los servicios lo pueden usar sin cambios.
"""
import pytest

from kuboerp import repositorios as contratos
from kuboerp.cotizaciones import InMemoryQuotationRepository
from kuboerp.inventario import InMemoryProductRepository, InventoryService, RegistroAlertas
from kuboerp.ordenes import InMemoryPurchaseOrderRepository
from kuboerp.proveedores import InMemoryOrderRepository, InMemorySupplierRepository
from kuboerp.talento_humano import InMemoryEmployeeRepository


@pytest.mark.parametrize("implementacion, contrato", [
    (InMemorySupplierRepository(), contratos.RepositorioProveedores),
    (InMemoryQuotationRepository(), contratos.RepositorioCotizaciones),
    (InMemoryPurchaseOrderRepository(), contratos.RepositorioOrdenes),
    (InMemoryPurchaseOrderRepository(), contratos.VerificadorOrdenesActivas),
    (InMemoryOrderRepository(), contratos.VerificadorOrdenesActivas),
    (InMemoryProductRepository(), contratos.RepositorioProductos),
    (InventoryService(), contratos.EntradaInventario),
    (RegistroAlertas(), contratos.ObservadorStock),
    (InMemoryEmployeeRepository(), contratos.RepositorioEmpleados),
], ids=lambda valor: getattr(valor, "__name__", type(valor).__name__))
def test_adaptador_cumple_el_contrato(implementacion, contrato):
    assert isinstance(implementacion, contrato)


def test_repositorio_minimo_de_ordenes_no_es_un_repositorio_completo():
    """Segregación de interfaces: el verificador mínimo solo sirve donde se pide VerificadorOrdenesActivas."""
    assert not isinstance(InMemoryOrderRepository(), contratos.RepositorioOrdenes)
