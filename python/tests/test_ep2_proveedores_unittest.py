"""Ejercicio práctico 2 · Tres pruebas unittest de SupplierService.create_supplier()."""
import unittest

from kuboerp.excepciones import InvalidSupplierException
from kuboerp.proveedores import SupplierService


class TestCreateSupplier(unittest.TestCase):
    def setUp(self):
        self.service = SupplierService()

    def test_nit_valido_crea_proveedor_activo(self):
        proveedor = self.service.create_supplier(
            "900123456", "Distribuidora Eléctrica del Centro", "compras@electrocentro.com.co")
        self.assertEqual(proveedor.estado, "ACTIVO")

    def test_nit_con_menos_de_9_caracteres_es_rechazado(self):
        with self.assertRaises(InvalidSupplierException):
            self.service.create_supplier("123", "Procables S.A.S.", "ventas@procables.com.co")

    def test_correo_sin_arroba_es_rechazado(self):
        with self.assertRaises(InvalidSupplierException):
            self.service.create_supplier("901555777", "Importadora LuzLED", "ventas.luzled.co")


if __name__ == "__main__":
    unittest.main()
