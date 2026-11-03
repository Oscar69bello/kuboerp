// Ejercicio 3 · InventoryService.registerProduct()
const InventoryService = require('../src/inventoryService');

describe('KuboERP · InventoryService - registro de productos', () => {
  let service;
  let mockRepo;

  const breaker = { codigo: 'BRK-2X30', nombre: 'Breaker 2x30A', categoria: 'Breakers y tableros', stock: 40 };

  beforeEach(() => {
    mockRepo = {
      findByCode: jest.fn(),
      save: jest.fn()
    };
    service = new InventoryService(mockRepo);
  });

  afterEach(() => jest.clearAllMocks());

  it('debería rechazar un producto con código duplicado', async () => {
    mockRepo.findByCode.mockResolvedValue({ ...breaker });

    await expect(service.registerProduct(breaker)).rejects.toThrow('El código ya está registrado');
    expect(mockRepo.findByCode).toHaveBeenCalledWith('BRK-2X30');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });

  it('debería llamar una sola vez a save cuando el producto es válido', async () => {
    mockRepo.findByCode.mockResolvedValue(null);
    mockRepo.save.mockImplementation(async (producto) => producto);

    const creado = await service.registerProduct(breaker);

    expect(mockRepo.save).toHaveBeenCalledTimes(1);
    expect(mockRepo.save).toHaveBeenCalledWith({ ...breaker, estado: 'DISPONIBLE' });
    expect(creado.estado).toBe('DISPONIBLE');
  });

  it('debería rechazar un stock inicial negativo sin consultar el repositorio', async () => {
    await expect(
      service.registerProduct({ ...breaker, codigo: 'LED-6060-48W', stock: -1 })
    ).rejects.toThrow('El stock inicial no puede ser negativo');
    expect(mockRepo.save).not.toHaveBeenCalled();
  });
});
