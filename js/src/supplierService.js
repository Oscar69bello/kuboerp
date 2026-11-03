// KuboERP · Servicio de proveedores (Taller 1)
const NIT_VALIDO = /^\d{9,10}$/;
const CORREO_VALIDO = /^[\w.+-]+@[\w-]+(\.[\w-]+)+$/;

class SupplierService {
  constructor(supplierRepo, orderRepo) {
    this.supplierRepo = supplierRepo;
    this.orderRepo = orderRepo;
  }

  async createSupplier({ nit, nombre, correo }) {
    if (!NIT_VALIDO.test(nit || '')) throw new Error('El NIT no es válido');
    if (!nombre || !nombre.trim()) throw new Error('El nombre es obligatorio');
    if (!CORREO_VALIDO.test(correo || '')) throw new Error('Formato de correo inválido');
    if (await this.supplierRepo.findByNit(nit)) throw new Error('El NIT ya está registrado');

    return this.supplierRepo.save({ nit, nombre, correo, estado: 'ACTIVO' });
  }

  async deleteSupplier(nit) {
    const proveedor = await this.supplierRepo.findByNit(nit);
    if (!proveedor) throw new Error('Proveedor no encontrado');
    if (await this.orderRepo.hasActiveOrders(nit)) {
      throw new Error('No se puede eliminar un proveedor con órdenes de compra activas');
    }
    await this.supplierRepo.save({ ...proveedor, estado: 'INACTIVO' });
    return 'Proveedor desactivado';
  }
}

module.exports = SupplierService;
