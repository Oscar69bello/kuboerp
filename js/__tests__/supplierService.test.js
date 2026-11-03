// Taller 1 · CRUD de proveedores (prueba unitaria con Jest)
const SupplierService = require('../src/supplierService');

describe('KuboERP · SupplierService', () => {
  let service;
  let supplierRepo;
  let orderRepo;

  beforeEach(() => {
    supplierRepo = { findByNit: jest.fn(), save: jest.fn() };
    orderRepo = { hasActiveOrders: jest.fn() };
    service = new SupplierService(supplierRepo, orderRepo);
  });

  afterEach(() => jest.clearAllMocks());

  it('deberiaCrearProveedorConCorreoValido', async () => {
    supplierRepo.findByNit.mockResolvedValue(null);
    supplierRepo.save.mockImplementation(async (p) => ({ id: 1, ...p }));

    const creado = await service.createSupplier({
      nit: '900123456',
      nombre: 'Distribuidora Eléctrica del Centro',
      correo: 'compras@electrocentro.com.co'
    });

    expect(supplierRepo.save).toHaveBeenCalledTimes(1);
    expect(supplierRepo.save).toHaveBeenCalledWith(expect.objectContaining({ estado: 'ACTIVO' }));
    expect(creado.estado).toBe('ACTIVO');
  });

  it('debería rechazar un correo con formato inválido', async () => {
    await expect(
      service.createSupplier({ nit: '901555777', nombre: 'Importadora LuzLED', correo: 'sin-arroba.com' })
    ).rejects.toThrow('Formato de correo inválido');
    expect(supplierRepo.save).not.toHaveBeenCalled();
  });

  it('no debería eliminar un proveedor con órdenes de compra activas', async () => {
    supplierRepo.findByNit.mockResolvedValue({ nit: '900888111', nombre: 'Procables S.A.S.', estado: 'ACTIVO' });
    orderRepo.hasActiveOrders.mockResolvedValue(true);

    await expect(service.deleteSupplier('900888111'))
      .rejects.toThrow('No se puede eliminar un proveedor con órdenes de compra activas');
    expect(supplierRepo.save).not.toHaveBeenCalled();
  });

  it('debería desactivar un proveedor sin órdenes de compra activas', async () => {
    supplierRepo.findByNit.mockResolvedValue({ nit: '901555777', nombre: 'Importadora LuzLED', estado: 'ACTIVO' });
    orderRepo.hasActiveOrders.mockResolvedValue(false);

    await expect(service.deleteSupplier('901555777')).resolves.toBe('Proveedor desactivado');
    expect(supplierRepo.save).toHaveBeenCalledWith(expect.objectContaining({ estado: 'INACTIVO' }));
  });
});
