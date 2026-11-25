# KuboERP · Imagen de la aplicación web ASP.NET Core MVC (.NET 10)
# Construcción en dos etapas: el SDK compila y publica; la imagen final solo lleva el runtime de ASP.NET.
#   docker build -t kuboerp-web:local .            (desde la carpeta dotnet/)

# ---------- Etapa 1: compilar y publicar ----------
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Primero solo el .csproj: la restauración de paquetes queda en caché mientras no cambien las dependencias
COPY KuboERP.Web/KuboERP.Web.csproj KuboERP.Web/
RUN dotnet restore KuboERP.Web/KuboERP.Web.csproj

COPY KuboERP.Web/ KuboERP.Web/
RUN dotnet publish KuboERP.Web/KuboERP.Web.csproj -c Release -o /app/publish /p:UseAppHost=false

# ---------- Etapa 2: imagen de ejecución ----------
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app

LABEL org.opencontainers.image.title="KuboERP" \
      org.opencontainers.image.description="ERP de ElectroSoluciones S.A.S.: compras, inventario y nómina" \
      org.opencontainers.image.source="https://github.com/Oscar69bello/kuboerp"

# Kestrel escucha en el puerto 8080 sin privilegios; el TLS lo pone el balanceador (Container Apps o Ingress)
ENV ASPNETCORE_HTTP_PORTS=8080 \
    ASPNETCORE_ENVIRONMENT=Production \
    DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false
EXPOSE 8080

COPY --from=build /app/publish .

# Usuario sin privilegios que trae la imagen oficial de .NET
USER $APP_UID

ENTRYPOINT ["dotnet", "KuboERP.Web.dll"]
