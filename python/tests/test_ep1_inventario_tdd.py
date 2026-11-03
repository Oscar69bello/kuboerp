"""Ejercicio práctico 1 · TDD de InventoryService.update_stock(product_id, quantity)."""
import unittest

from kuboerp.excepciones import InsufficientStockException
from kuboerp.inventario import InventoryService


class TestUpdateStock(unittest.TestCase):
    def setUp(self):
        self.service = InventoryService()
        self.service.register_product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 40)
        self.service.register_product("TOMA-DOBLE-PT", "Toma doble con polo a tierra", "Interruptores y tomas", 2)

    def test_salida_que_deja_stock_negativo_lanza_excepcion(self):
        with self.assertRaises(InsufficientStockException):
            self.service.update_stock("TOMA-DOBLE-PT", -5)
        self.assertEqual(self.service.stock_de("TOMA-DOBLE-PT"), 2)

    def test_salida_valida_resta_del_stock(self):
        self.assertEqual(self.service.update_stock("BRK-2X30", -5), 35)

    def test_entrada_suma_al_stock(self):
        self.assertEqual(self.service.update_stock("BRK-2X30", 10), 50)


if __name__ == "__main__":
    unittest.main()
