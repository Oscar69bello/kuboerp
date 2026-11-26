# Guion del video · KuboERP en Visual Studio

**Duración estimada:** 14 minutos · **Grabación:** Microsoft Teams · **Herramienta:** solo Visual Studio 2026

Cómo leer este guion:
- 🖱️ **Hacer**: lo que se hace en pantalla.
- 🗣️ **Decir**: texto sugerido; no hace falta leerlo palabra por palabra.
- ✅ **Se debe ver**: el resultado esperado, para saber que todo va bien.

---

## PARTE 0 · Preparación (antes de grabar, 10 minutos)

### 0.1 Datos limpios
1. Abrir `C:\KuboERP\dotnet\KuboERP.slnx` en Visual Studio y **maximizar** la ventana.
2. En el selector junto al ▶ verde elegir **«Reiniciar datos de ejemplo»** y pulsar **Ctrl + F5**.
3. Cuando abra el navegador, cerrarlo y detener la app (**Mayús + F5** o cerrar la consola).
4. Volver a elegir el perfil **https** (el que ya funciona en este equipo).

> Si se hacen pruebas antes de grabar, repetir este paso: el guion usa los datos de ejemplo tal como vienen.

### 0.2 Dejar Visual Studio listo
1. **Explorador de soluciones** (Ctrl + Alt + L): un clic en **KuboERP.Web** y tecla **→**. Dejar **Dependencias** y **Connected Services** cerrados.
2. Cerrar todas las pestañas del editor. Abrir **Program.cs** y **Services → Compras.cs**.
3. Cerrar los paneles **Tabulaciones** y **Propiedades** (✕) para ganar espacio.
4. Zoom del código en **125 %** (abajo a la izquierda del editor).
5. Abrir **Ver → Explorador de objetos de SQL Server** y expandir
   `SQL Server → (localdb)\MSSQLLocalDB → Bases de datos → KuboERP → Tablas`.

### 0.3 Equipo
- Cerrar programas que no se usen y activar **No molestar** en Windows.
- Cámara y micrófono probados, buena luz de frente.
- Usar la cuenta **institucional** de Teams (`@ucundinamarca.edu.co`).

### 0.4 Iniciar la grabación en Teams
1. Teams → **Calendario → Reunirse ahora**, con la **cámara encendida**.
2. **Compartir → Pantalla** (pantalla completa).
3. **Modo de moderador → Destacado**: la cara queda encima de la pantalla compartida.
4. **Más (…) → Grabar y transcribir → Iniciar grabación**.
5. Comprobar en los primeros segundos que la cara se ve sobre Visual Studio.

> ⚠️ Nota = 1,0 si no se ve el rostro, si no se graba en Teams o si el video no está en SharePoint. **Nunca apagar la cámara.**

---

## PARTE 1 · Presentación (0:00 – 0:45)

🖱️ Visual Studio en pantalla, con el Explorador de soluciones abierto.

🗣️ «Buenas tardes, profesor Carlos Eduardo Mujica Reyes. Soy Oscar Javier Bello Daza, de Ingeniería de Sistemas y
Computación de la Universidad de Cundinamarca, extensión Chía, en la materia Proyecto de Ingeniería de Software II.
Voy a presentar **KuboERP**, un sistema de planificación de recursos empresariales que no está hecho para una empresa
en particular: los datos que verán son de una empresa ficticia del sector eléctrico. El ERP está desarrollado completamente en
**Visual Studio** con **C#**, **ASP.NET Core MVC**, **Entity Framework Core** y base de datos **SQL Server**. Integra
los módulos de **compras, inventario y talento humano con nómina**.»

---

## PARTE 2 · La solución en Visual Studio (0:45 – 2:30)

🖱️ Señalar el Explorador de soluciones.

🗣️ «La solución **KuboERP** tiene dos proyectos: **KuboERP.Specs**, con las pruebas de comportamiento BDD, y
**KuboERP.Web**, que es el ERP. El proyecto está organizado por capas:»

| 🖱️ Señalar | 🗣️ Decir |
|---|---|
| **Models** | «Las entidades, que son las tablas de la base de datos: proveedor, producto, orden de compra, empleado y desprendible de nómina.» |
| **Data** | «El contexto de Entity Framework, que se conecta con SQL Server, y los datos de ejemplo de la empresa.» |
| **Services** | «La lógica de negocio. Aquí están las reglas: por ejemplo, que una orden no supere el presupuesto del proveedor.» |
| **Controllers** | «Reciben lo que hace el usuario en la página y llaman a los servicios.» |
| **Views** | «Las pantallas, hechas en Razor, que mezcla HTML y C#.» |
| **wwwroot** | «Los estilos y la identidad visual de KuboERP.» |
| **appsettings.json** | «La cadena de conexión a SQL Server.» |

🖱️ Abrir **Program.cs**.

🗣️ «En **Program.cs** se registra la base de datos SQL Server, los servicios del ERP, y al arrancar se crea la base de
datos con los datos de ejemplo.»

🖱️ Abrir **Services → Compras.cs**, **Ctrl + F**, buscar `AprobarAsync`.

🗣️ «Este es un ejemplo de regla de negocio. Al aprobar una orden de compra, si el monto es mayor que el presupuesto del
proveedor, el sistema lo impide. Si alcanza, descuenta el monto del presupuesto y deja el cambio en la auditoría. Las
reglas viven en los servicios y no en las pantallas: así se respeta la separación de responsabilidades de SOLID.»

🗣️ «Los candados que se ven en los archivos indican que el proyecto está bajo control de versiones con **Git**, en
GitHub.»

---

## PARTE 3 · La base de datos (2:30 – 3:15)

🖱️ Clic en **Explorador de objetos de SQL Server** (pestaña vertical de la izquierda) → **Tablas**.

🗣️ «La base de datos **KuboERP** está en SQL Server. Estas son sus tablas: Proveedores, Productos, Órdenes, Líneas de
orden, Cotizaciones, Movimientos de inventario, Empleados y Desprendibles de nómina.»

🖱️ Clic derecho en **dbo.Proveedores → Ver datos**.

✅ Se ven 5 proveedores; *Ferretería La Sabana* está INACTIVO.

🗣️ «Aquí están los proveedores guardados. Al final del video vamos a volver para comprobar que todo lo que hagamos queda
en la base de datos.»

---

## PARTE 4 · Ejecutar y tablero gerencial (3:15 – 4:00)

🖱️ Pulsar el **▶ verde** (perfil https).

🗣️ «Ejecuto el proyecto desde Visual Studio. Visual Studio compila KuboERP, lo levanta en el servidor local,
localhost, y abre el navegador.»

✅ Se abre el **Tablero gerencial**.

🗣️ «El tablero gerencial muestra el pulso de la empresa: las compras del mes, el valor del inventario, los
productos en stock crítico y el costo de la última nómina. Abajo están las alertas de stock crítico, ordenadas de la
más urgente a la menos urgente, el valor del inventario por categoría y las últimas órdenes y movimientos.»

✅ Dice **3 productos en stock crítico**: Breaker bipolar 2x30 A, Reflector LED 100 W y Cable THHN calibre 10.

---

## PARTE 5 · Proveedores (4:00 – 5:30)

🖱️ Menú **Proveedores**.

🗣️ «Este es el CRUD de proveedores, con búsqueda y filtro por estado.»

**Crear con error:** 🖱️ **Nuevo proveedor** → NIT `123`, nombre `Prueba`, correo `prueba` → **Guardar**.

✅ Mensajes en rojo: el NIT debe tener 9 o 10 dígitos y el correo no es válido.

🗣️ «El sistema valida el NIT y el formato del correo.»

**Crear bien:** 🖱️ Corregir:

| Campo | Valor |
|---|---|
| NIT | `901555777` |
| Razón social | `Soluciones Solares del Norte` |
| Correo | `ventas@solaresnorte.co` |
| Teléfono | `607 300 1122` |
| Presupuesto | `7000000` |

✅ «Proveedor Soluciones Solares del Norte registrado exitosamente».

**Eliminar con historial:** 🖱️ En **Eléctricos del Centro S.A.S.** pulsar la 🗑️ → **Aceptar**.

✅ «…tiene órdenes o cotizaciones: no se elimina, queda INACTIVO».

🗣️ «Un proveedor con órdenes o cotizaciones no se borra, para no perder el historial: queda inactivo.»

🖱️ Clic en su nombre → **Reactivar**.

🗣️ «Y se puede reactivar desde su ficha, donde también se ven sus órdenes y cotizaciones.»

---

## PARTE 6 · Cotizaciones (5:30 – 7:00)

🖱️ Menú **Cotizaciones** → abrir **SOL-2026-002 · Reposición de breakers y diferenciales**.

🗣️ «Para comprar, primero se abre una solicitud de cotización y los proveedores envían sus ofertas. Este es el cuadro
comparativo: Protecciones Industriales cotizó 1.420.000 pesos y Eléctricos del Centro 1.310.000.»

🖱️ En **Registrar cotización**: proveedor **Soluciones Solares del Norte**, monto `1250000`, días `5` → **Registrar**.

✅ La nueva cotización aparece con la etiqueta **MEJOR PRECIO**.

🖱️ Intentar registrar otra de **Protecciones Industriales Ltda.**, monto `1000000`.

✅ «Regla de negocio: El proveedor ya cotizó esta solicitud».

🗣️ «Cada proveedor cotiza una sola vez por solicitud.»

🖱️ En la de **Soluciones Solares del Norte** pulsar **Seleccionar**.

✅ Queda **SELECCIONADA**, las demás **RECHAZADAS** y la solicitud **CERRADA**.

🗣️ «Al elegir la ganadora, las demás quedan rechazadas automáticamente y la solicitud se cierra.»

---

## PARTE 7 · Órdenes de compra (7:00 – 9:30)

**Crear desde la cotización:** 🖱️ En la cotización seleccionada pulsar **Crear orden**.

| Producto | Cantidad | Precio |
|---|---|---|
| `BRK-2X30 · Breaker bipolar 2x30 A` | `20` | 52.000 (sale solo) |
| `DIF-2X40 · Interruptor diferencial 2x40 A` | `5` | 168.000 (sale solo) |

✅ El total se calcula solo: **$ 1.880.000**, contra un presupuesto de $ 7.000.000.

🖱️ **Crear orden** → ✅ queda en **PENDIENTE**. 🖱️ **Aprobar orden**.

✅ Queda **APROBADA** y el presupuesto del proveedor baja a **$ 5.120.000**.

🗣️ «El ciclo de vida de una orden es pendiente, aprobada y recibida. Al aprobar se descuenta el presupuesto.»

**Presupuesto insuficiente:** 🖱️ Menú **Órdenes de compra** → **OC-2026-004** (Protecciones Industriales) → **Aprobar orden**.

✅ «Presupuesto insuficiente: la orden vale $ 2.610.000 y el proveedor tiene $ 2.500.000».

🗣️ «Si la orden supera el presupuesto del proveedor, no se aprueba.»

**Recibir mercancía:** 🖱️ **OC-2026-003** (Eléctricos del Centro, $ 1.942.000) → **Aprobar orden** → **Registrar recepción de mercancía**.

✅ Queda **RECIBIDA** y la **Auditoría de estados** muestra Creación → APROBADA → RECIBIDA.

🗣️ «Al recibir la mercancía, el sistema genera automáticamente las entradas en el inventario: 4 tableros y 50 tubos
EMT. Cada cambio de estado queda auditado.»

**Cancelar:** 🖱️ **OC-2026-002** (Iluminación LED Colombia, APROBADA) → escribir la justificación
`El cliente aplazó la obra para enero` → **Cancelar orden**.

✅ Queda **CANCELADA** y el presupuesto del proveedor sube a **$ 11.564.000**.

🗣️ «Cancelar exige una justificación y, si la orden estaba aprobada, devuelve el monto al presupuesto.»

---

## PARTE 8 · Inventario (9:30 – 11:00)

🖱️ Menú **Inventario**.

🗣️ «El inventario muestra cada producto con su stock, su mínimo, una barra de nivel y el valor en bodega. Los productos
en rojo están en stock crítico.»

🖱️ Señalar **Tablero de distribución 12 circuitos** (13) y **Tubo EMT** (170).

🗣️ «Estos dos subieron por la orden que acabamos de recibir.»

**Retiro excesivo:** 🖱️ Abrir **Panel LED 18 W luz blanca** (stock 64, mínimo 25) → cantidad `500` → **Retiro**.

✅ «Stock insuficiente: hay 64 unidades…».

**Retiro que deja stock crítico:** 🖱️ Cantidad `45`, detalle `Despacho a obra Los Robles` → **Retiro**.

✅ «⚠ Panel LED 18 W quedó en stock crítico (19 de mínimo 25). Se sugiere comprar 31 unidades».

🗣️ «No se puede retirar más de lo que hay. Cuando un producto llega a su mínimo, el sistema avisa y sugiere cuánto
comprar.»

🖱️ Mostrar el **Kárdex del producto** (a la derecha) y volver a **Inventario** → activar **Solo stock crítico**.

🗣️ «Cada movimiento queda en el kárdex con el saldo resultante. Con este filtro, el jefe de compras ve qué reponer.»

---

## PARTE 9 · Empleados (11:00 – 11:45)

🖱️ Menú **Empleados** → **Nuevo empleado**:

| Campo | Valor |
|---|---|
| Cédula | `1012345678` |
| Nombre | `Andrés Felipe Castro` |
| Cargo | Técnico electricista |
| Contrato | FIJO |
| Salario | `1000000` |

🖱️ **Guardar** → ✅ «El salario no puede ser inferior al salario mínimo ($ 1.750.905)».

🖱️ Cambiar salario a `2300000` → **Guardar** → ✅ registrado.

🗣️ «El salario se valida contra el mínimo legal de 2026. La ARL se asigna según el riesgo: los técnicos de campo son
clase 4.»

🖱️ En **Santiago Gómez Ortiz** pulsar **Desvincular** → **Aceptar**.

🗣️ «Un empleado desvinculado no se borra: queda retirado y ya no entra en la nómina.»

---

## PARTE 10 · Nómina (11:45 – 13:00)

🖱️ Menú **Nómina**.

🗣️ «Aquí está la nómina de octubre ya liquidada, con el devengado, las deducciones, el neto y lo que le cuesta cada
empleado a la empresa.»

🖱️ **Liquidar nómina** (periodo noviembre 2026) y llenar las novedades:

| Empleado | Novedad |
|---|---|
| Jorge Andrés Peña (técnico) | Horas extra: `10` |
| Paola Andrea Ruiz (asesora) | Ventas: `30000000` |
| Laura Camila Rincón (gerente) | Bonificación: `4000000` |

🖱️ **Calcular y guardar nómina** → ✅ «Nómina de 2026-11 liquidada para 6 empleados».

🗣️ «Santiago ya no aparece porque lo desvinculamos, y Andrés sí porque lo acabamos de contratar.»

🖱️ **Desprendible** de **Jorge Andrés Peña**.

✅ Devengado **$ 2.780.556** · auxilio de transporte **$ 249.095** · salud y pensión **$ 111.222** cada una · neto **$ 2.807.207**.

🗣️ «El motor de nómina aplica la normativa colombiana 2026: horas extra con recargo del 25 %, auxilio de transporte para
quien gana hasta dos salarios mínimos, salud y pensión del 4 %, y los aportes del empleador. Para la gerente aplica el
fondo de solidaridad pensional y los aportes a salud, SENA e ICBF, porque gana más de diez salarios mínimos.»

---

## PARTE 11 · Volver a la base de datos (13:00 – 13:45)

🖱️ Volver a **Visual Studio** → **Explorador de objetos de SQL Server** → clic derecho → **Ver datos** en:
- **dbo.Proveedores** → ✅ aparece *Soluciones Solares del Norte* con presupuesto $ 5.120.000.
- **dbo.Ordenes** → ✅ la orden nueva y los estados RECIBIDA y CANCELADA.
- **dbo.Desprendibles** → ✅ las filas del periodo 2026-11.

🗣️ «Todo lo que hicimos en la aplicación quedó guardado en SQL Server.»

---

## PARTE 12 · Cierre (13:45 – 14:15)

🖱️ Volver al **Tablero gerencial** del navegador.

🗣️ «Así queda KuboERP: compras con cotizaciones y órdenes con control de presupuesto, inventario con alertas de
stock crítico y talento humano con nómina, todo integrado sobre una sola base de datos SQL Server y desarrollado en
Visual Studio con C# y ASP.NET Core. Muchas gracias, profesor.»

🖱️ Teams → **Detener grabación** → salir de la reunión.

---

## PARTE 13 · Compartir el enlace sin perder puntos

1. En el chat de la reunión abrir la grabación (se abre en **Stream**, que es SharePoint).
2. **Compartir → Configuración del vínculo** → **«Personas de Universidad de Cundinamarca»** (o **«Cualquier persona»**
   si está disponible) → permiso **«Puede ver»**. Así el docente no tiene que pedir acceso.
3. **Copiar vínculo**: debe empezar por `https://ucundinamarca-my.sharepoint.com/...`.
4. **Acortarlo** en <https://tinyurl.com> con el alias `KuboERP-OscarBello` →
   `https://tinyurl.com/KuboERP-OscarBello`.
5. **Probarlo** desde otra cuenta de la universidad o con un compañero: debe reproducir el video al primer clic.

| Regla de la nota | Cómo se cumple |
|---|---|
| Rostro visible todo el tiempo (si no, 1,0) | Cámara encendida + modo **Destacado** |
| Grabado en Teams y alojado en SharePoint (si no, 1,0) | **Grabar y transcribir** con la cuenta institucional |
| El enlace debe abrir el video (si no, 1,0) | Permiso **Puede ver** para la universidad, y probarlo |
| Enlace acortado (−0,5) | Alias de TinyURL |
| Cada clic extra (−0,5 por clic) | Copiar el vínculo del **video**, no de la carpeta |

## Si algo sale mal mientras grabas

| Problema | Qué hacer |
|---|---|
| Un mensaje en rojo que no esperabas | Leerlo en voz alta: es una regla de negocio y también suma. |
| Te equivocas de dato | Corregir en vivo y seguir; no hace falta repetir. |
| La app no abre | Detener (Mayús + F5), revisar que no haya otra ventana de consola abierta y pulsar ▶ otra vez. |
| Se apaga la cámara | Detener la grabación y empezar de nuevo: sin rostro la nota es 1,0. |
