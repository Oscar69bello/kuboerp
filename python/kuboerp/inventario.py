"""CRUD de inventario y control de stock crítico (EP01-US04, EP07-US02, EP07-US03, EP07-US04).

El Ejercicio 1 del taller de TDD creó update_stock() con el ciclo Rojo → Verde → Refactor. El taller de
Sprint Planning y CRUD agrega:
* stock mínimo por producto y estado CRÍTICO cuando el stock llega al mínimo o baja de él;
* alertas con el patrón Observer: el servicio avisa a quien se suscriba (tablero, correo, compras) sin
  conocerlo (SOLID · O: se agregan observadores nuevos sin modificar el servicio);
* consulta, actualización e inactivación lógica de productos.
"""
from dataclasses import dataclass

from kuboerp.excepciones import InsufficientStockException, InvalidProductException

MSG_RETIRO_EXITOSO = "Retiro exitoso"
MSG_STOCK_INSUFICIENTE = "Stock insuficiente"
MSG_INACTIVADO = "Producto inactivado"


@dataclass
class Product:
    codigo: str
    nombre: str
    categoria: str
    stock: int = 0
    stock_minimo: int = 0
    estado: str = "ACTIVO"

    @property
    def es_critico(self):
        return self.stock_minimo > 0 and self.stock <= self.stock_minimo


@dataclass(frozen=True)
class AlertaStock:
    codigo: str
    nombre: str
    stock: int
    stock_minimo: int

    @property
    def cantidad_sugerida(self):
        """Cantidad para reponer hasta el doble del stock mínimo (insumo de la orden de compra)."""
        return self.stock_minimo * 2 - self.stock


class RegistroAlertas:
    """Observador que guarda las alertas; lo usan el tablero de Almacén y las pruebas."""

    def __init__(self):
        self.alertas = []

    def notificar(self, alerta):
        self.alertas.append(alerta)


class InMemoryProductRepository:
    def __init__(self):
        self._datos = {}
        self.movimientos = []

    def save(self, producto):
        self._datos[producto.codigo] = producto
        return producto

    def find_by_code(self, codigo):
        return self._datos.get(codigo)

    def find_all(self):
        return list(self._datos.values())


class InventoryService:
    def __init__(self, repo=None):
        self.repo = repo if repo is not None else InMemoryProductRepository()
        self._observadores = []

    def suscribir(self, observador):
        self._observadores.append(observador)

    # ---------- C ----------
    def register_product(self, codigo, nombre, categoria, stock=0, stock_minimo=0):
        if not codigo:
            raise InvalidProductException("El código es obligatorio")
        if not categoria:
            raise InvalidProductException("La categoría es obligatoria")
        if stock < 0:
            raise InvalidProductException("El stock inicial no puede ser negativo")
        self._validar_minimo(stock_minimo)
        if self.repo.find_by_code(codigo) is not None:
            raise InvalidProductException("El código ya está registrado")
        return self.repo.save(Product(codigo, nombre, categoria, stock, stock_minimo))

    def update_stock(self, product_id, quantity):
        """Suma (entrada) o resta (salida, cantidad negativa) unidades al stock."""
        producto = self._buscar(product_id)
        if producto.estado != "ACTIVO":
            raise InvalidProductException("El producto está inactivo")
        nuevo_stock = producto.stock + quantity
        self._validar_stock_resultante(nuevo_stock)
        producto.stock = nuevo_stock
        self.repo.save(producto)
        self.repo.movimientos.append((product_id, quantity))
        if quantity < 0 and producto.es_critico:
            self._avisar(producto)
        return producto.stock

    def retirar(self, codigo, cantidad):
        self.update_stock(codigo, -cantidad)
        return MSG_RETIRO_EXITOSO

    # ---------- R ----------
    def stock_de(self, codigo):
        return self._buscar(codigo).stock

    def buscar(self, codigo):
        return self._buscar(codigo)

    def listar(self, categoria=None, incluir_inactivos=False):
        return sorted((p for p in self.repo.find_all()
                       if (categoria is None or p.categoria == categoria)
                       and (incluir_inactivos or p.estado == "ACTIVO")),
                      key=lambda p: p.codigo)

    def productos_criticos(self):
        """Productos activos en stock crítico, del más urgente (menor cobertura) al menos urgente."""
        criticos = [p for p in self.listar() if p.es_critico]
        return sorted(criticos, key=lambda p: p.stock / p.stock_minimo)

    # ---------- U ----------
    def actualizar_producto(self, codigo, nombre=None, categoria=None, stock_minimo=None):
        producto = self._buscar(codigo)
        if nombre is not None:
            if not nombre.strip():
                raise InvalidProductException("El nombre es obligatorio")
            producto.nombre = nombre.strip()
        if categoria is not None:
            if not categoria:
                raise InvalidProductException("La categoría es obligatoria")
            producto.categoria = categoria
        if stock_minimo is not None:
            self._validar_minimo(stock_minimo)
            producto.stock_minimo = stock_minimo
            if producto.es_critico:
                self._avisar(producto)
        return self.repo.save(producto)

    # ---------- D (lógico) ----------
    def inactivar_producto(self, codigo):
        producto = self._buscar(codigo)
        if producto.stock > 0:
            raise InvalidProductException("El producto tiene existencias sin ajustar")
        producto.estado = "INACTIVO"
        self.repo.save(producto)
        return MSG_INACTIVADO

    # ---------- apoyo ----------
    def _buscar(self, codigo):
        producto = self.repo.find_by_code(codigo)
        if producto is None:
            raise InvalidProductException("Producto no encontrado")
        return producto

    def _avisar(self, producto):
        alerta = AlertaStock(producto.codigo, producto.nombre, producto.stock, producto.stock_minimo)
        for observador in self._observadores:
            observador.notificar(alerta)

    @staticmethod
    def _validar_minimo(stock_minimo):
        if stock_minimo < 0:
            raise InvalidProductException("El stock mínimo no puede ser negativo")

    @staticmethod
    def _validar_stock_resultante(nuevo_stock):
        if nuevo_stock < 0:
            raise InsufficientStockException(MSG_STOCK_INSUFICIENTE)
