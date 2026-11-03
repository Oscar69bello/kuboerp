// Taller 2 · Solicitud de cotizaciones: prueba parametrizada con it.each
const QuotationService = require('../src/quotationService');

describe('KuboERP · QuotationService - validar monto de cotización', () => {
  let service;
  let mockRepo;

  beforeEach(() => {
    mockRepo = {
      findRequest: jest.fn().mockResolvedValue({ codigo: 'SC-0001', producto: 'Panel LED 60x60 48W', estado: 'ABIERTA' }),
      existsByRequestAndSupplier: jest.fn().mockResolvedValue(false),
      save: jest.fn().mockResolvedValue(undefined)
    };
    service = new QuotationService(mockRepo);
  });

  afterEach(() => jest.clearAllMocks());

  it.each([
    [2500000, 'Cotización registrada'],
    [0, 'Monto inválido'],
    [-1000, 'Monto inválido']
  ])('monto %p → "%s"', async (monto, resultado) => {
    const cotizacion = { solicitud: 'SC-0001', nitProveedor: '901555777', monto };

    if (monto > 0) {
      await expect(service.register(cotizacion)).resolves.toBe(resultado);
      expect(mockRepo.save).toHaveBeenCalledTimes(1);
    } else {
      await expect(service.register(cotizacion)).rejects.toThrow(resultado);
      expect(mockRepo.save).not.toHaveBeenCalled();
    }
  });

  it('debería rechazar una cotización sobre una solicitud que no está ABIERTA', async () => {
    mockRepo.findRequest.mockResolvedValue({ codigo: 'SC-0002', estado: 'CERRADA' });

    await expect(service.register({ solicitud: 'SC-0002', nitProveedor: '901555777', monto: 2300000 }))
      .rejects.toThrow('La solicitud no está abierta');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });

  it('debería rechazar una segunda cotización del mismo proveedor para la misma solicitud', async () => {
    mockRepo.existsByRequestAndSupplier.mockResolvedValue(true);

    await expect(service.register({ solicitud: 'SC-0001', nitProveedor: '901555777', monto: 2300000 }))
      .rejects.toThrow('El proveedor ya cotizó esta solicitud');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });
});
