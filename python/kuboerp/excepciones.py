"""Excepciones de negocio de KuboERP (Compras, Logística y Almacén)."""


class InvalidSupplierException(Exception):
    """El proveedor no cumple las reglas de registro."""


class SupplierHasActiveOrdersException(Exception):
    """El proveedor tiene órdenes de compra activas y no se puede eliminar."""


class InvalidQuotationException(Exception):
    """La cotización no cumple las reglas de registro."""


class PurchaseOrderException(Exception):
    """La orden de compra no se puede aprobar."""


class InvalidProductException(Exception):
    """El producto no cumple las reglas del inventario."""


class InsufficientStockException(Exception):
    """El retiro supera el stock disponible."""
