"""Taller 2 · Solicitudes y cotizaciones de proveedores."""
from dataclasses import dataclass

from kuboerp.excepciones import InvalidQuotationException

MSG_REGISTRADA = "Cotización registrada"


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
        return any(c.solicitud == solicitud and c.nit_proveedor == nit for c in self.cotizaciones)

    def save(self, cotizacion):
        self.cotizaciones.append(cotizacion)
        return cotizacion


class QuotationService:
    def __init__(self, repo=None):
        self.repo = repo if repo is not None else InMemoryQuotationRepository()

    def registrar(self, codigo, solicitud, nit_proveedor, monto):
        if self.repo.find_request(solicitud) != "ABIERTA":
            raise InvalidQuotationException("La solicitud no está abierta")
        if monto <= 0:
            raise InvalidQuotationException("Monto inválido")
        if self.repo.exists_by_request_and_supplier(solicitud, nit_proveedor):
            raise InvalidQuotationException("El proveedor ya cotizó esta solicitud")
        return self.repo.save(Quotation(codigo, solicitud, nit_proveedor, monto))
