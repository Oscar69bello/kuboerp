# language: es
# Taller 1 · CRUD de Proveedores (Mockup 3 · Compras, Logística y Almacén)
Característica: Gestión de proveedores de material eléctrico en KuboERP
  Como jefe de compras de la empresa
  Quiero registrar proveedores con NIT y correo válidos
  Para mantener actualizada la base de fabricantes, mayoristas e importadores

  Escenario: Registrar un proveedor válido
    Dado que no existe un proveedor con NIT "900123456"
    Cuando registro el proveedor con NIT "900123456", nombre "Distribuidora Eléctrica del Centro" y correo "compras@electrocentro.com.co"
    Entonces el proveedor se crea con estado "ACTIVO"
    Y el sistema muestra "Proveedor registrado exitosamente"

  Escenario: Rechazar proveedor con NIT duplicado
    Dado que ya existe un proveedor con NIT "900123456"
    Cuando intento registrar otro proveedor con el mismo NIT
    Entonces el sistema muestra "El NIT ya está registrado"
    Y no se crea un nuevo proveedor

  Esquema del escenario: Validar formatos de correo
    Cuando registro un proveedor con correo "<correo>"
    Entonces el sistema responde "<resultado>"

    Ejemplos:
      | correo                       | resultado                  |
      | ventas@importadoraluzled.com | Correo válido              |
      | sin-arroba.com               | Formato de correo inválido |
      | usuario@                     | Formato de correo inválido |

  Escenario: Eliminar proveedor sin órdenes activas
    Dado que existe un proveedor "Importadora LuzLED" con NIT "901555777" sin órdenes de compra activas
    Cuando solicito eliminar el proveedor
    Entonces el proveedor cambia a estado "INACTIVO"
    Y el sistema confirma "Proveedor desactivado"

  Escenario: No eliminar proveedor con órdenes activas
    Dado que existe un proveedor "Procables S.A.S." con NIT "900888111" y la orden de compra "OC-0001" en estado "PENDIENTE"
    Cuando solicito eliminar el proveedor
    Entonces el sistema muestra "No se puede eliminar un proveedor con órdenes de compra activas"
    Y el proveedor sigue en estado "ACTIVO"
