using System.Globalization;
using KuboERP.Web.Data;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.AspNetCore.Localization;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();

// Base de datos SQL Server: LocalDB en Visual Studio, contenedor de SQL Server en Docker y Kubernetes,
// Azure SQL en la nube. La cadena llega por la variable de entorno ConnectionStrings__KuboERP.
builder.Services.AddDbContext<KuboDbContext>(o =>
    o.UseSqlServer(builder.Configuration.GetConnectionString("KuboERP"),
        sql => sql.EnableRetryOnFailure(maxRetryCount: 6, maxRetryDelay: TimeSpan.FromSeconds(10), errorNumbersToAdd: null)));

// Sonda de salud para Docker, Kubernetes y Azure Container Apps
builder.Services.AddHealthChecks().AddCheck<BaseDeDatosHealthCheck>("sql", tags: new[] { "listo" });

// Detrás de un balanceador (Container Apps, Ingress de Kubernetes) el TLS termina en el proxy:
// se confía en X-Forwarded-Proto para que la app sepa que la petición original fue https.
builder.Services.Configure<ForwardedHeadersOptions>(o =>
{
    o.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    o.KnownIPNetworks.Clear();
    o.KnownProxies.Clear();
});

// Servicios de dominio: las reglas de negocio viven aquí, no en los controladores
builder.Services.AddScoped<ProveedorService>();
builder.Services.AddScoped<CotizacionService>();
builder.Services.AddScoped<InventarioService>();
builder.Services.AddScoped<OrdenCompraService>();
builder.Services.AddScoped<EmpleadoService>();
builder.Services.AddScoped<NominaService>();

var app = builder.Build();

// Crea la base de datos y carga los datos de ejemplo la primera vez.
// En contenedores SQL Server puede tardar en arrancar, así que se reintenta durante un minuto.
for (var intento = 1; ; intento++)
{
    try
    {
        using var scope = app.Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<KuboDbContext>();
        // Perfil "Reiniciar datos de ejemplo": borra la base y la vuelve a crear limpia (útil antes de una demostración)
        if (builder.Configuration.GetValue<bool>("ReiniciarDatos"))
            db.Database.EnsureDeleted();
        db.Database.EnsureCreated();
        DatosIniciales.Cargar(db);
        break;
    }
    catch (Exception ex) when (intento < 20)
    {
        app.Logger.LogWarning("Base de datos no disponible (intento {Intento}/20): {Mensaje}", intento, ex.Message);
        Thread.Sleep(TimeSpan.FromSeconds(3));
    }
}

app.UseForwardedHeaders();

var colombia = new CultureInfo("es-CO");
app.UseRequestLocalization(new RequestLocalizationOptions
{
    DefaultRequestCulture = new RequestCulture(colombia),
    SupportedCultures = new[] { colombia },
    SupportedUICultures = new[] { colombia }
});

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
    // En producción todo va por https; en desarrollo se permite http para no depender del certificado local
    app.UseHttpsRedirection();
}
app.UseRouting();
app.UseAuthorization();
app.MapStaticAssets();

// /health/vivo: el proceso responde (liveness). /health: además hay conexión con SQL Server (readiness).
app.MapHealthChecks("/health/vivo", new HealthCheckOptions { Predicate = _ => false });
app.MapHealthChecks("/health", new HealthCheckOptions { Predicate = r => r.Tags.Contains("listo") });

app.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();
