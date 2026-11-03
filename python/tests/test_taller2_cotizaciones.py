"""Taller 2 · Validar el monto de una cotización con @pytest.mark.parametrize."""
from unittest.mock import MagicMock

import pytest

from kuboerp.cotizaciones import QuotationService
from kuboerp.excepciones import InvalidQuotationException


@pytest.fixture
def repo():
    repo = MagicMock()
    repo.find_request.return_value = "ABIERTA"
    repo.exists_by_request_and_supplier.return_value = False
    repo.save.side_effect = lambda cotizacion: cotizacion
    return repo


@pytest.mark.parametrize("monto,resultado", [
    (2500000, "Cotización registrada"),
    (0, "Monto inválido"),
    (-1000, "Monto inválido"),
], ids=["monto_2500000", "monto_0", "monto_negativo_1000"])
def test_validar_monto_de_cotizacion(repo, monto, resultado):
    service = QuotationService(repo)

    if monto > 0:
        cotizacion = service.registrar("COT-0001", "SC-0001", "901555777", monto)
        assert cotizacion.estado == "RECIBIDA"
        assert resultado == "Cotización registrada"
        repo.save.assert_called_once()
    else:
        with pytest.raises(InvalidQuotationException, match=resultado):
            service.registrar("COT-0001", "SC-0001", "901555777", monto)
        repo.save.assert_not_called()


def test_rechaza_cotizacion_sobre_solicitud_cerrada(repo):
    repo.find_request.return_value = "CERRADA"

    with pytest.raises(InvalidQuotationException, match="La solicitud no está abierta"):
        QuotationService(repo).registrar("COT-0002", "SC-0002", "901555777", 2300000)
    repo.save.assert_not_called()


def test_rechaza_segunda_cotizacion_del_mismo_proveedor(repo):
    repo.exists_by_request_and_supplier.return_value = True

    with pytest.raises(InvalidQuotationException, match="El proveedor ya cotizó esta solicitud"):
        QuotationService(repo).registrar("COT-0003", "SC-0001", "901555777", 2300000)
    repo.save.assert_not_called()
