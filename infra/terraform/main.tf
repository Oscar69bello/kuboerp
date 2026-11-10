# KuboERP · Infraestructura como código del ambiente de pruebas en Azure.
#
# Recursos: grupo de recursos, App Service (Linux, Python 3.12) con identidad administrada,
# Azure SQL con autenticación exclusiva de Microsoft Entra ID, Key Vault con RBAC y
# Application Insights sobre Log Analytics. Ver docs/arquitectura/arc42.md, secciones 7 y 8.

data "azurerm_client_config" "actual" {}

resource "random_string" "sufijo" {
  length  = 5
  upper   = false
  special = false
}

locals {
  prefijo   = "kuboerp-${var.ambiente}"
  sufijo    = random_string.sufijo.result
  etiquetas = merge(var.etiquetas, { ambiente = var.ambiente })
}

resource "azurerm_resource_group" "kubo" {
  name     = "rg-${local.prefijo}"
  location = var.ubicacion
  tags     = local.etiquetas
}

# ---------------------------------------------------------------- observabilidad
resource "azurerm_log_analytics_workspace" "kubo" {
  name                = "log-${local.prefijo}-${local.sufijo}"
  location            = azurerm_resource_group.kubo.location
  resource_group_name = azurerm_resource_group.kubo.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.etiquetas
}

resource "azurerm_application_insights" "kubo" {
  name                = "appi-${local.prefijo}-${local.sufijo}"
  location            = azurerm_resource_group.kubo.location
  resource_group_name = azurerm_resource_group.kubo.name
  workspace_id        = azurerm_log_analytics_workspace.kubo.id
  application_type    = "web"
  tags                = local.etiquetas
}

# ---------------------------------------------------------------- datos
resource "azurerm_mssql_server" "kubo" {
  name                          = "sql-${local.prefijo}-${local.sufijo}"
  resource_group_name           = azurerm_resource_group.kubo.name
  location                      = azurerm_resource_group.kubo.location
  version                       = "12.0"
  minimum_tls_version           = "1.2"
  public_network_access_enabled = true
  tags                          = local.etiquetas

  # Sin usuario y contraseña de SQL: solo identidades de Microsoft Entra ID (RNF de seguridad del Sprint 1).
  azuread_administrator {
    login_username              = var.sql_admin_login
    object_id                   = var.sql_admin_object_id
    azuread_authentication_only = true
  }
}

resource "azurerm_mssql_database" "kubo" {
  name        = "sqldb-${local.prefijo}"
  server_id   = azurerm_mssql_server.kubo.id
  sku_name    = "Basic"
  max_size_gb = 2
  tags        = local.etiquetas

  short_term_retention_policy {
    retention_days = 7
  }
}

# Permite el tráfico que sale de servicios de Azure (App Service); no abre la base a Internet.
resource "azurerm_mssql_firewall_rule" "servicios_azure" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.kubo.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# ---------------------------------------------------------------- secretos
resource "azurerm_key_vault" "kubo" {
  name                       = "kv-kubo-${var.ambiente}-${local.sufijo}"
  location                   = azurerm_resource_group.kubo.location
  resource_group_name        = azurerm_resource_group.kubo.name
  tenant_id                  = data.azurerm_client_config.actual.tenant_id
  sku_name                   = "standard"
  enable_rbac_authorization  = true
  purge_protection_enabled   = true
  soft_delete_retention_days = 7
  tags                       = local.etiquetas
}

# ---------------------------------------------------------------- aplicación
resource "azurerm_service_plan" "kubo" {
  name                = "asp-${local.prefijo}"
  location            = azurerm_resource_group.kubo.location
  resource_group_name = azurerm_resource_group.kubo.name
  os_type             = "Linux"
  sku_name            = var.sku_app_service
  tags                = local.etiquetas
}

resource "azurerm_linux_web_app" "kubo" {
  name                = "app-${local.prefijo}-${local.sufijo}"
  location            = azurerm_resource_group.kubo.location
  resource_group_name = azurerm_resource_group.kubo.name
  service_plan_id     = azurerm_service_plan.kubo.id
  https_only          = true
  tags                = local.etiquetas

  identity {
    type = "SystemAssigned"
  }

  site_config {
    minimum_tls_version = "1.2"
    ftps_state          = "Disabled"
    http2_enabled       = true

    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    APPLICATIONINSIGHTS_CONNECTION_STRING = azurerm_application_insights.kubo.connection_string
    KUBO_AMBIENTE                         = var.ambiente
    KUBO_SQL_SERVIDOR                     = azurerm_mssql_server.kubo.fully_qualified_domain_name
    KUBO_SQL_BASE_DATOS                   = azurerm_mssql_database.kubo.name
    KUBO_KEY_VAULT_URI                    = azurerm_key_vault.kubo.vault_uri
  }
}

# Mínimo privilegio: la aplicación solo puede leer secretos del Key Vault, no administrarlo.
resource "azurerm_role_assignment" "app_lee_secretos" {
  scope                = azurerm_key_vault.kubo.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.kubo.identity[0].principal_id
}
