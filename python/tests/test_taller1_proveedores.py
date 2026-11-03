"""Taller 1 · Eliminar (desactivar) proveedores, con el repositorio de órdenes simulado."""
import unittest
from unittest.mock import MagicMock

import pytest

from kuboerp.excepciones import SupplierHasActiveOrdersException
from kuboerp.proveedores import SupplierService


class TestEliminarProveedor(unittest.TestCase):
    def test_no_deberia_eliminar_con_ordenes_activas(self):
        repo_ordenes = MagicMock()
        repo_ordenes.has_active_orders.return_value = True
        service = SupplierService(repo_ordenes=repo_ordenes)
        service.create_supplier("900888111", "Procables S.A.S.", "ventas@procables.com.co")

        with self.assertRaises(SupplierHasActiveOrdersException):
            service.delete_supplier("900888111")
        self.assertEqual(service.buscar("900888111").estado, "ACTIVO")

    def test_deberia_desactivar_proveedor_sin_ordenes_activas(self):
        repo_ordenes = MagicMock()
        repo_ordenes.has_active_orders.return_value = False
        service = SupplierService(repo_ordenes=repo_ordenes)
        service.create_supplier("901555777", "Importadora LuzLED", "ventas@importadoraluzled.com")

        mensaje = service.delete_supplier("901555777")

        self.assertEqual(mensaje, "Proveedor desactivado")
        self.assertEqual(service.buscar("901555777").estado, "INACTIVO")
        repo_ordenes.has_active_orders.assert_called_once_with("901555777")


# Ejemplo de la sección 3: fixture + parametrización + mock con pytest
@pytest.fixture
def supplier_service():
    repo = MagicMock()
    return SupplierService(repo)


@pytest.mark.parametrize("nit,esperado", [
    ("900123456", True),
    ("123", False),
    ("", False),
])
def test_validar_nit(supplier_service, nit, esperado):
    assert supplier_service.es_nit_valido(nit) == esperado
