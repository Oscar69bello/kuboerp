output "url_aplicacion" {
  description = "URL HTTPS del App Service del ambiente."
  value       = "https://${azurerm_linux_web_app.kubo.default_hostname}"
}

output "servidor_sql" {
  description = "Nombre completo del servidor de Azure SQL."
  value       = azurerm_mssql_server.kubo.fully_qualified_domain_name
}

output "key_vault_uri" {
  description = "URI del Key Vault donde se guardan los secretos de la aplicación."
  value       = azurerm_key_vault.kubo.vault_uri
}
