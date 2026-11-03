// KuboERP · Servicio de inventario de material eléctrico (Ejercicio 3)
class InventoryService {
  constructor(productRepo) {
    this.productRepo = productRepo;
  }

  async registerProduct({ codigo, nombre, categoria, stock }) {
    if (!codigo) throw new Error('El código es obligatorio');
    if (!categoria) throw new Error('La categoría es obligatoria');
    if (!Number.isInteger(stock) || stock < 0) throw new Error('El stock inicial no puede ser negativo');
    if (await this.productRepo.findByCode(codigo)) throw new Error('El código ya está registrado');

    return this.productRepo.save({ codigo, nombre, categoria, stock, estado: 'DISPONIBLE' });
  }
}

module.exports = InventoryService;
