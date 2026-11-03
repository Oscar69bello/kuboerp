"""Taller 4 · Retiro de inventario recorriendo los casos del esquema con subTest."""
import unittest

from kuboerp.excepciones import InsufficientStockException, InvalidProductException
from kuboerp.inventario import InventoryService

CASOS = [
    # codigo,          stock, retiro, final, mensaje
    ("CAB-THHN-12",    10,    3,      7,     "Retiro exitoso"),
    ("BRK-2X30",       5,     5,      0,     "Retiro exitoso"),
    ("TOMA-DOBLE-PT",  2,     5,      2,     "Stock insuficiente"),
]


class TestRetiroInventario(unittest.TestCase):
    def test_retiro_de_inventario(self):
        for codigo, stock, retiro, final, mensaje in CASOS:
            with self.subTest(codigo=codigo, stock=stock, retiro=retiro):
                service = InventoryService()
                service.register_product(codigo, f"Producto {codigo}", "Material eléctrico", stock)

                if retiro > stock:
                    with self.assertRaises(InsufficientStockException) as error:
                        service.retirar(codigo, retiro)
                    self.assertEqual(str(error.exception), mensaje)
                else:
                    self.assertEqual(service.retirar(codigo, retiro), mensaje)
                self.assertEqual(service.stock_de(codigo), final)

    def test_no_registra_codigo_duplicado(self):
        service = InventoryService()
        service.register_product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 40)
        with self.assertRaises(InvalidProductException):
            service.register_product("BRK-2X30", "Otro breaker", "Breakers y tableros", 5)

    def test_no_registra_sin_categoria_ni_con_stock_negativo(self):
        service = InventoryService()
        with self.assertRaises(InvalidProductException):
            service.register_product("LED-6060-48W", "Panel LED 60x60 48W", "", 10)
        with self.assertRaises(InvalidProductException):
            service.register_product("LED-6060-48W", "Panel LED 60x60 48W", "Iluminación", -1)


if __name__ == "__main__":
    unittest.main()
