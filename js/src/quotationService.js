// KuboERP · Servicio de cotizaciones de proveedores (Taller 2)
class QuotationService {
  constructor(quotationRepo) {
    this.quotationRepo = quotationRepo;
  }

  async register({ solicitud, nitProveedor, monto }) {
    const solicitudCompra = await this.quotationRepo.findRequest(solicitud);
    if (!solicitudCompra || solicitudCompra.estado !== 'ABIERTA') {
      throw new Error('La solicitud no está abierta');
    }
    if (!(monto > 0)) throw new Error('Monto inválido');
    if (await this.quotationRepo.existsByRequestAndSupplier(solicitud, nitProveedor)) {
      throw new Error('El proveedor ya cotizó esta solicitud');
    }

    await this.quotationRepo.save({ solicitud, nitProveedor, monto });
    return 'Cotización registrada';
  }
}

module.exports = QuotationService;
