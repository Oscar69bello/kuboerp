// KuboERP · Servicio de aprobación de órdenes de compra (Taller 3)
class PurchaseOrderService {
  constructor(orderRepo) {
    this.orderRepo = orderRepo;
  }

  async approve(id) {
    const orden = await this.orderRepo.findById(id);
    if (!orden) throw new Error('Orden no encontrada');
    if (orden.estado === 'APROBADA') throw new Error('La orden ya está aprobada');

    const presupuesto = await this.orderRepo.getBudget(orden.proveedorId);
    if (orden.monto > presupuesto) throw new Error('Presupuesto insuficiente');

    return this.orderRepo.save({ ...orden, estado: 'APROBADA' });
  }
}

module.exports = PurchaseOrderService;
