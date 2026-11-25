using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace KuboERP.Web.Data;

/// <summary>
/// Sonda de salud: responde "Healthy" en /health cuando la aplicación puede conectarse a SQL Server.
/// La usan el healthcheck de Docker Compose, las sondas readiness/liveness de Kubernetes y Azure Container Apps.
/// </summary>
public class BaseDeDatosHealthCheck : IHealthCheck
{
    private readonly KuboDbContext db;

    public BaseDeDatosHealthCheck(KuboDbContext db) => this.db = db;

    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        try
        {
            return await db.Database.CanConnectAsync(cancellationToken)
                ? HealthCheckResult.Healthy("SQL Server disponible")
                : HealthCheckResult.Unhealthy("No hay conexión con SQL Server");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Error al conectar con SQL Server", ex);
        }
    }
}
