using System.Globalization;
using KuboERP.Web.Data;
using KuboERP.Web.Services;
using Microsoft.AspNetCore.Localization;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();

// Base de datos SQL Server (LocalDB en desarrollo; Azure SQL en el ambiente de pruebas)
builder.Services.AddDbContext<KuboDbContext>(o =>
    o.UseSqlServer(builder.Configuration.GetConnectionString("KuboERP")));

// Servicios de dominio: las reglas de negocio viven aquí, no en los controladores
builder.Services.AddScoped<ProveedorService>();
builder.Services.AddScoped<CotizacionService>();
builder.Services.AddScoped<InventarioService>();
builder.Services.AddScoped<OrdenCompraService>();
builder.Services.AddScoped<EmpleadoService>();
builder.Services.AddScoped<NominaService>();

var app = builder.Build();

// Crea la base de datos y carga los datos de ejemplo la primera vez
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<KuboDbContext>();
    // Perfil "Reiniciar datos de ejemplo": borra la base y la vuelve a crear limpia (útil antes de una demostración)
    if (builder.Configuration.GetValue<bool>("ReiniciarDatos"))
        db.Database.EnsureDeleted();
    db.Database.EnsureCreated();
    DatosIniciales.Cargar(db);
}

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
}

app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthorization();
app.MapStaticAssets();

app.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();
