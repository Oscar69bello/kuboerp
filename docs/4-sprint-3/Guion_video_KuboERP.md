# Video de KuboERP en Visual Studio · guion y lista de chequeo

Entrega: video grabado en **Microsoft Teams**, alojado en **SharePoint/OneDrive de la universidad**, con el
**rostro visible todo el tiempo**, mostrando el ERP **solo desde Visual Studio** (C#, ASP.NET Core, SQL Server).

## 1. Antes de grabar (10 minutos)

1. Abrir `C:\KuboERP\dotnet\KuboERP.slnx` en **Visual Studio Community 2026**.
2. En la barra superior, junto al botón verde ▶, elegir el perfil **«Reiniciar datos de ejemplo»** y pulsar ▶ una vez.
   La base de datos queda limpia con los datos de ElectroSoluciones S.A.S. Cerrar el navegador y detener (■).
3. Volver a elegir el perfil **«http»**. Ese es el que se usa en el video (no pide certificado).
4. Abrir **Ver → Explorador de objetos de SQL Server** y expandir
   `(localdb)\MSSQLLocalDB → Bases de datos → KuboERP → Tablas`. Dejarlo listo.
5. Cerrar todo lo que no sea Visual Studio y el navegador que abre la app. Silenciar notificaciones
   (Windows: «No molestar»).
6. Usar la cuenta **institucional** de Teams (`@ucundinamarca.edu.co`), no la personal: así la grabación
   queda en el OneDrive/SharePoint de la universidad.

## 2. Grabar en Teams con el rostro siempre visible

1. Teams → **Calendario → Reunirse ahora**. Encender la **cámara** antes de entrar.
2. **Compartir → Pantalla** (la pantalla completa, no una ventana: así se ve Visual Studio y el navegador).
3. En la barra de la reunión elegir **Modo de moderador → Destacado** (*Standout*): el rostro queda
   superpuesto sobre la pantalla compartida y **sale en la grabación**.
4. **Más (…) → Grabar y transcribir → Iniciar grabación**.
5. Verificar en los primeros segundos que la cara se ve sobre el contenido. Si no, detener y repetir.
6. Al terminar: **Detener grabación** y salir de la reunión. El video aparece en el chat de la reunión
   en unos minutos.

> Nota = 1,0 si no se ve el rostro, si no se graba en Teams o si no está en SharePoint. No cortar la cámara
> en ningún momento.

## 3. Recorrido (≈ 12 minutos)

| Min | Qué mostrar | Ejemplo para decir y hacer |
|---|---|---|
| 0:00 | Presentación con cámara | Nombre, materia, «KuboERP para ElectroSoluciones S.A.S., desarrollado en Visual Studio con C#, ASP.NET Core MVC, Entity Framework Core y SQL Server». |
| 0:45 | **Visual Studio: la solución** | Explorador de soluciones: `KuboERP.Web` (Models, Data, Services, Controllers, Views) y `KuboERP.Specs` (pruebas BDD). Abrir `Services/Compras.cs` → método `AprobarAsync`: «las reglas de negocio viven en servicios, no en los controladores». |
| 2:00 | **Base de datos** | Explorador de objetos de SQL Server → tabla `Proveedores` → *Ver datos*. «Entity Framework crea la base en LocalDB; en Azure será Azure SQL». Mostrar la cadena de conexión en `appsettings.json`. |
| 2:45 | Ejecutar con ▶ | Se abre el **Tablero gerencial**: compras del mes, valor del inventario, stock crítico, costo de la nómina, alertas y últimas órdenes. |
| 3:30 | **Proveedores** | Crear *Soluciones Solares del Norte*, NIT `901555777`, `ventas@solaresnorte.co`, presupuesto `7000000`. Probar un NIT de 3 dígitos → error. Eliminar *Eléctricos del Centro* → queda **INACTIVO** porque tiene órdenes. Reactivarlo desde su detalle. |
| 5:00 | **Cotizaciones** | Abrir `SOL-2026-002`. Registrar una cotización de *Soluciones Solares del Norte* por `1250000`. Intentar que *Protecciones Industriales* cotice otra vez → «ya cotizó». Seleccionar la de mejor precio → las otras quedan **RECHAZADAS** y la solicitud **CERRADA**. |
| 6:30 | **Órdenes de compra** | Abrir `OC-2026-004` → **Aprobar** → «Presupuesto insuficiente» ($ 2.610.000 contra $ 2.500.000). Abrir `OC-2026-003` → Aprobar → el presupuesto del proveedor baja. **Registrar recepción** → mostrar la auditoría de estados. Crear una orden nueva con 2 productos y ver el total calculado. Cancelar una con justificación. |
| 8:30 | **Inventario** | Ver los productos en rojo (stock crítico). Abrir *Panel LED 18 W* → retirar `500` → «Stock insuficiente». Retirar `45` → aviso de **stock crítico** con cantidad sugerida. Mostrar el **kárdex**. Mostrar que los productos de `OC-2026-003` aumentaron. |
| 10:00 | **Empleados** | Crear un técnico con salario `1000000` → «no puede ser inferior al salario mínimo». Corregir a `2300000`. Desvincular a uno. |
| 10:45 | **Nómina** | *Liquidar nómina* noviembre: 10 horas extra al técnico, ventas de `30000000` al asesor, bonificación de `4000000` a la gerente. Abrir el **desprendible**: auxilio de transporte, IBC, salud y pensión del 4 %, aportes del empleador. |
| 11:45 | **Vuelta a la base de datos** | En Visual Studio, *Ver datos* de `Ordenes`, `Movimientos` y `Desprendibles`: «todo lo que hicimos quedó guardado en SQL Server». |
| 12:15 | Cierre | Resumen de los módulos y despedida. |

## 4. Compartir el enlace sin perder puntos

1. En el chat de la reunión, abrir la grabación (se abre en **Stream**, que es SharePoint).
2. **Compartir → Configuración del vínculo**: elegir **«Personas de Universidad de Cundinamarca»**
   (o **«Cualquier persona»** si la universidad lo permite) y permiso **«Puede ver»**. Así el docente no tiene
   que pedir acceso (cada clic extra resta 0,5).
3. **Copiar vínculo**. Debe empezar por `https://ucundinamarca-my.sharepoint.com/...` o `https://ucundinamarca.sharepoint.com/...`.
4. **Acortarlo** (si el enlace es largo resta 0,5): en <https://tinyurl.com> pegar el vínculo y poner el alias
   `KuboERP-OscarBello`. Queda `https://tinyurl.com/KuboERP-OscarBello`, que redirige directo al video, sin clics
   adicionales.
5. **Probar el enlace** en una ventana de incógnito con otra cuenta de la universidad, o pedirle a un compañero que lo
   abra: debe reproducir el video al primer clic. Si pide permiso, revisar el paso 2.

## 5. Lista de chequeo antes de entregar

- [ ] Grabado en Teams con la cuenta institucional
- [ ] Rostro visible de principio a fin (modo Destacado)
- [ ] Todo se muestra desde Visual Studio: código, base de datos y la app ejecutada con ▶
- [ ] Se recorrieron todos los módulos con ejemplos
- [ ] Video alojado en SharePoint/OneDrive de la universidad
- [ ] Permiso «Puede ver» para la universidad; el enlace abre el video sin pedir acceso
- [ ] Enlace acortado con alias corto
- [ ] Enlace probado desde otra cuenta
