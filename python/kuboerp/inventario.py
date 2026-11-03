"""Taller 4 y Ejercicio 1 · Inventario de productos, materia prima e insumos eléctricos.

Versión final del ciclo TDD (después del Refactor): la validación del stock se
extrajo a _validar_stock_resultante() y retirar() reutiliza update_stock().
"""
from dataclasses import dataclass

from kuboerp.excepciones import InsufficientStockException, InvalidProductException

MSG_RETIRO_EXITOSO = "Retiro exitoso"
MSG_STOCK_INSUFICIENTE = "Stock insuficiente"


@dataclass
class Product:
    codigo: str
    nombre: str
    categoria: str
    stock: int = 0


class InMemoryProductRepository:
    def __init__(self):
        self._datos = {}
        self.movimientos = []

    def save(self, producto):
        self._datos[producto.codigo] = producto
        return producto

    def find_by_code(self, codigo):
        return self._datos.get(codigo)


class InventoryService:
    def __init__(self, repo=None):
        self.repo = repo if repo is not None else InMemoryProductRepository()

    def register_product(self, codigo, nombre, categoria, stock=0):
        if not codigo:
            raise InvalidProductException("El código es obligatorio")
        if not categoria:
            raise InvalidProductException("La categoría es obligatoria")
        if stock < 0:
            raise InvalidProductException("El stock inicial no puede ser negativo")
        if self.repo.find_by_code(codigo) is not None:
            raise InvalidProductException("El código ya está registrado")
        return self.repo.save(Product(codigo, nombre, categoria, stock))

    def update_stock(self, product_id, quantity):
        """Suma (entrada) o resta (salida, cantidad negativa) unidades al stock."""
        producto = self._buscar(product_id)
        nuevo_stock = producto.stock + quantity
        self._validar_stock_resultante(nuevo_stock)
        producto.stock = nuevo_stock
        self.repo.save(producto)
        self.repo.movimientos.append((product_id, quantity))
        return producto.stock

    def retirar(self, codigo, cantidad):
        self.update_stock(codigo, -cantidad)
        return MSG_RETIRO_EXITOSO

    def stock_de(self, codigo):
        return self._buscar(codigo).stock

    def _buscar(self, codigo):
        producto = self.repo.find_by_code(codigo)
        if producto is None:
            raise InvalidProductException("Producto no encontrado")
        return producto

    @staticmethod
    def _validar_stock_resultante(nuevo_stock):
        if nuevo_stock < 0:
            raise InsufficientStockException(MSG_STOCK_INSUFICIENTE)
