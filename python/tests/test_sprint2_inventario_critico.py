"""Sprint 2 · CRUD de inventario y control de stock crítico (unittest).

Se usa unittest (incluido en Python) para que el archivo corra igual en Google Colab, en el computador y
en GitHub Actions sin instalar nada.
"""
import unittest

from kuboerp.excepciones import InsufficientStockException, InvalidProductException
from kuboerp.inventario import AlertaStock, InventoryService, RegistroAlertas


class TestStockCritico(unittest.TestCase):
    def setUp(self):
        self.inventario = InventoryService()
        self.alertas = RegistroAlertas()
        self.inventario.suscribir(self.alertas)
        self.inventario.register_product("CAB-THHN-12", "Cable THHN 12 AWG (rollo 100 m)", "Cables", 30, 10)
        self.inventario.register_product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 40, 15)
        self.inventario.register_product("LED-6060-48W", "Panel LED 60x60 48W", "Iluminación", 8, 0)

    def test_retiro_que_deja_el_stock_en_el_minimo_genera_alerta(self):
        self.inventario.retirar("CAB-THHN-12", 20)

        self.assertEqual(self.alertas.alertas, [AlertaStock("CAB-THHN-12", "Cable THHN 12 AWG (rollo 100 m)",
                                                            10, 10)])
        self.assertTrue(self.inventario.buscar("CAB-THHN-12").es_critico)

    def test_retiro_que_no_llega_al_minimo_no_genera_alerta(self):
        self.inventario.retirar("CAB-THHN-12", 19)
        self.assertEqual(self.alertas.alertas, [])

    def test_las_entradas_no_generan_alerta(self):
        self.inventario.retirar("CAB-THHN-12", 25)        # queda en 5: alerta
        self.inventario.update_stock("CAB-THHN-12", 2)    # entrada: sigue crítico, sin alerta nueva
        self.assertEqual(len(self.alertas.alertas), 1)

    def test_producto_sin_minimo_nunca_es_critico(self):
        self.inventario.retirar("LED-6060-48W", 8)
        self.assertFalse(self.inventario.buscar("LED-6060-48W").es_critico)
        self.assertEqual(self.alertas.alertas, [])

    def test_cantidad_sugerida_repone_hasta_el_doble_del_minimo(self):
        self.inventario.retirar("CAB-THHN-12", 26)
        self.assertEqual(self.alertas.alertas[0].cantidad_sugerida, 16)   # 2 x 10 - 4

    def test_productos_criticos_del_mas_urgente_al_menos_urgente(self):
        self.inventario.retirar("CAB-THHN-12", 22)   # 8/10  = 0,80
        self.inventario.retirar("BRK-2X30", 31)      # 9/15  = 0,60
        criticos = [p.codigo for p in self.inventario.productos_criticos()]
        self.assertEqual(criticos, ["BRK-2X30", "CAB-THHN-12"])

    def test_subir_el_minimo_por_encima_del_stock_genera_alerta(self):
        self.inventario.actualizar_producto("LED-6060-48W", stock_minimo=12)
        self.assertEqual(self.alertas.alertas[0].codigo, "LED-6060-48W")

    def test_varios_observadores_reciben_la_misma_alerta(self):
        tablero = RegistroAlertas()
        self.inventario.suscribir(tablero)
        self.inventario.retirar("BRK-2X30", 30)
        self.assertEqual(self.alertas.alertas, tablero.alertas)

    def test_minimo_negativo_rechazado(self):
        with self.assertRaisesRegex(InvalidProductException, "stock mínimo no puede ser negativo"):
            self.inventario.register_product("TOMA-DOBLE-PT", "Toma doble", "Interruptores y tomas", 5, -1)


class TestInventarioCrud(unittest.TestCase):
    def setUp(self):
        self.inventario = InventoryService()
        self.inventario.register_product("CAB-THHN-12", "Cable THHN 12 AWG", "Cables", 30, 10)
        self.inventario.register_product("BRK-2X30", "Breaker 2x30A", "Breakers y tableros", 0, 5)
        self.inventario.register_product("CAB-THHN-10", "Cable THHN 10 AWG", "Cables", 12, 4)

    def test_listar_por_categoria_ordenado_por_codigo(self):
        codigos = [p.codigo for p in self.inventario.listar("Cables")]
        self.assertEqual(codigos, ["CAB-THHN-10", "CAB-THHN-12"])

    def test_actualizar_nombre_y_categoria(self):
        producto = self.inventario.actualizar_producto("CAB-THHN-12", nombre=" Cable THHN 12 AWG negro ",
                                                       categoria="Cables y alambres")
        self.assertEqual(producto.nombre, "Cable THHN 12 AWG negro")
        self.assertEqual(producto.categoria, "Cables y alambres")

    def test_actualizar_con_datos_vacios(self):
        with self.assertRaisesRegex(InvalidProductException, "El nombre es obligatorio"):
            self.inventario.actualizar_producto("CAB-THHN-12", nombre="  ")
        with self.assertRaisesRegex(InvalidProductException, "La categoría es obligatoria"):
            self.inventario.actualizar_producto("CAB-THHN-12", categoria="")

    def test_inactivar_producto_sin_existencias(self):
        self.assertEqual(self.inventario.inactivar_producto("BRK-2X30"), "Producto inactivado")
        self.assertNotIn("BRK-2X30", [p.codigo for p in self.inventario.listar()])
        self.assertIn("BRK-2X30", [p.codigo for p in self.inventario.listar(incluir_inactivos=True)])

    def test_no_inactivar_producto_con_existencias(self):
        with self.assertRaisesRegex(InvalidProductException, "existencias sin ajustar"):
            self.inventario.inactivar_producto("CAB-THHN-12")

    def test_producto_inactivo_no_recibe_movimientos(self):
        self.inventario.inactivar_producto("BRK-2X30")
        with self.assertRaisesRegex(InvalidProductException, "El producto está inactivo"):
            self.inventario.update_stock("BRK-2X30", 10)

    def test_retiro_mayor_al_stock_no_cambia_el_kardex(self):
        with self.assertRaises(InsufficientStockException):
            self.inventario.retirar("CAB-THHN-10", 13)
        self.assertEqual(self.inventario.repo.movimientos, [])


if __name__ == "__main__":
    unittest.main()
