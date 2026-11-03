// Plantilla del taller aplicada a KuboERP · aprobación de órdenes de compra con mock del repositorio
const PurchaseOrderService = require('../src/purchaseOrderService');

describe('KuboERP · PurchaseOrderService - aprobación', () => {
  let service;
  let mockRepo;

  beforeEach(() => {
    mockRepo = {
      findById: jest.fn(),
      save: jest.fn(),
      getBudget: jest.fn()
    };
    service = new PurchaseOrderService(mockRepo);
  });

  afterEach(() => jest.clearAllMocks());

  it('debería aprobar la OC-0001 de Distribuidora Eléctrica del Centro dentro del presupuesto', async () => {
    mockRepo.findById.mockResolvedValue({ id: 'OC-0001', monto: 5000000, estado: 'PENDIENTE', proveedorId: '900123456' });
    mockRepo.getBudget.mockResolvedValue(10000000);
    mockRepo.save.mockResolvedValue({ id: 'OC-0001', estado: 'APROBADA' });

    const orden = await service.approve('OC-0001');

    expect(orden.estado).toBe('APROBADA');
    expect(mockRepo.save).toHaveBeenCalledTimes(1);
  });

  it('debería rechazar una orden que excede el presupuesto', async () => {
    mockRepo.findById.mockResolvedValue({ id: 'OC-0002', monto: 15000000, estado: 'PENDIENTE', proveedorId: '900123456' });
    mockRepo.getBudget.mockResolvedValue(10000000);

    await expect(service.approve('OC-0002')).rejects.toThrow('Presupuesto insuficiente');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });

  it('no debería aprobar una orden ya aprobada', async () => {
    mockRepo.findById.mockResolvedValue({ id: 'OC-0003', monto: 1000000, estado: 'APROBADA' });

    await expect(service.approve('OC-0003')).rejects.toThrow('La orden ya está aprobada');
  });
});
