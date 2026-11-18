"""Excepciones de negocio de KuboERP (Compras, Logística, Almacén y Talento Humano)."""


class InvalidSupplierException(Exception):
    """El proveedor no cumple las reglas de registro."""


class SupplierHasActiveOrdersException(Exception):
    """El proveedor tiene órdenes de compra activas y no se puede eliminar."""


class InvalidQuotationException(Exception):
    """La cotización no cumple las reglas de registro."""


class PurchaseOrderException(Exception):
    """La orden de compra no se puede crear o no se puede cambiar de estado."""


class InvalidProductException(Exception):
    """El producto no cumple las reglas del inventario."""


class InsufficientStockException(Exception):
    """El retiro supera el stock disponible."""


class InvalidEmployeeException(Exception):
    """El empleado no cumple las reglas de registro o de contrato."""
