"""CRUD de solicitudes y cotizaciones de proveedores (EP05-US07).

Ciclo de vida de una cotización:  RECIBIDA → SELECCIONADA | RECHAZADA | ANULADA
Al seleccionar la cotización ganadora, las demás de la misma solicitud quedan RECHAZADAS y la solicitud
pasa a CERRADA, de modo que ya no recibe cotizaciones.
"""
from dataclasses import dataclass

from kuboerp.excepciones import InvalidQuotationException

MSG_REGISTRADA = "Cotización registrada"
MSG_ANULADA = "Cotización anulada"


@dataclass
class Quotation:
    codigo: str
    solicitud: str
    nit_proveedor: str
    monto: int
    estado: str = "RECIBIDA"


class InMemoryQuotationRepository:
    def __init__(self):
        self.solicitudes = {}      # código → estado ("ABIERTA", "CERRADA")
        self.cotizaciones = []

    def add_request(self, codigo, estado="ABIERTA"):
        self.solicitudes[codigo] = estado

    def find_request(self, codigo):
        return self.solicitudes.get(codigo)

    def exists_by_request_and_supplier(self, solicitud, nit):
        return any(c.solicitud == solicitud and c.nit_proveedor == nit and c.estado != "ANULADA"
                   for c in self.cotizaciones)

    def find_by_codigo(self, codigo):
        return next((c for c in self.cotizaciones if c.codigo == codigo), None)

    def find_by_request(self, solicitud):
        return [c for c in self.cotizaciones if c.solicitud == solicitud]

    def save(self, cotizacion):
        if cotizacion not in self.cotizaciones:
            self.cotizaciones.append(cotizacion)
        return cotizacion


class QuotationService:
    def __init__(self, repo=None):
        self.repo = repo if repo is not None else InMemoryQuotationRepository()

    # ---------- C ----------
    def abrir_solicitud(self, codigo):
        if not codigo:
            raise InvalidQuotationException("El código de la solicitud es obligatorio")
        if self.repo.find_request(codigo) is not None:
            raise InvalidQuotationException("La solicitud ya existe")
        self.repo.add_request(codigo)
        return codigo

    def registrar(self, codigo, solicitud, nit_proveedor, monto):
        if self.repo.find_request(solicitud) != "ABIERTA":
            raise InvalidQuotationException("La solicitud no está abierta")
        if monto <= 0:
            raise InvalidQuotationException("Monto inválido")
        if self.repo.find_by_codigo(codigo) is not None:
            raise InvalidQuotationException("El código de la cotización ya existe")
        if self.repo.exists_by_request_and_supplier(solicitud, nit_proveedor):
            raise InvalidQuotationException("El proveedor ya cotizó esta solicitud")
        return self.repo.save(Quotation(codigo, solicitud, nit_proveedor, monto))

    # ---------- R ----------
    def buscar(self, codigo):
        cotizacion = self.repo.find_by_codigo(codigo)
        if cotizacion is None:
            raise InvalidQuotationException("Cotización no encontrada")
        return cotizacion

    def listar_por_solicitud(self, solicitud):
        """Cotizaciones vigentes de la solicitud, de la más barata a la más cara."""
        vigentes = [c for c in self.repo.find_by_request(solicitud) if c.estado != "ANULADA"]
        return sorted(vigentes, key=lambda c: c.monto)

    # ---------- U ----------
    def actualizar_monto(self, codigo, monto):
        cotizacion = self._buscar_recibida(codigo)
        if monto <= 0:
            raise InvalidQuotationException("Monto inválido")
        cotizacion.monto = monto
        return self.repo.save(cotizacion)

    def seleccionar(self, codigo):
        """Elige la cotización ganadora, rechaza las demás y cierra la solicitud."""
        ganadora = self._buscar_recibida(codigo)
        for otra in self.repo.find_by_request(ganadora.solicitud):
            if otra.estado == "RECIBIDA":
                otra.estado = "RECHAZADA"
                self.repo.save(otra)
        ganadora.estado = "SELECCIONADA"
        self.repo.add_request(ganadora.solicitud, "CERRADA")
        return self.repo.save(ganadora)

    # ---------- D (lógico) ----------
    def anular(self, codigo):
        cotizacion = self._buscar_recibida(codigo)
        cotizacion.estado = "ANULADA"
        self.repo.save(cotizacion)
        return MSG_ANULADA

    def _buscar_recibida(self, codigo):
        cotizacion = self.buscar(codigo)
        if cotizacion.estado != "RECIBIDA":
            raise InvalidQuotationException("Solo se modifican cotizaciones en estado RECIBIDA")
        return cotizacion
