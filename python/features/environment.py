"""Behave · prepara servicios nuevos (en memoria) antes de cada escenario."""
from kuboerp.cotizaciones import InMemoryQuotationRepository, QuotationService
from kuboerp.inventario import InventoryService
from kuboerp.ordenes import InMemoryPurchaseOrderRepository, PurchaseOrderService
from kuboerp.proveedores import InMemorySupplierRepository, SupplierService


def before_scenario(context, scenario):
    context.repo_proveedores = InMemorySupplierRepository()
    context.repo_ordenes = InMemoryPurchaseOrderRepository()
    context.repo_cotizaciones = InMemoryQuotationRepository()

    context.proveedores = SupplierService(context.repo_proveedores, context.repo_ordenes)
    context.ordenes = PurchaseOrderService(context.repo_proveedores, context.repo_ordenes)
    context.cotizaciones = QuotationService(context.repo_cotizaciones)
    context.inventario = InventoryService()

    context.mensaje = None
    context.excepcion = None

    def ejecutar(accion):
        """Ejecuta el paso @when y guarda el mensaje de éxito o el de la excepción."""
        try:
            context.mensaje = accion()
            context.excepcion = None
        except Exception as error:  # noqa: BLE001 - el escenario verifica el mensaje
            context.excepcion = error
            context.mensaje = str(error)

    context.ejecutar = ejecutar
