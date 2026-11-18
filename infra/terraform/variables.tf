variable "ambiente" {
  description = "Ambiente que se despliega: dev o test (la Definition of Done exige el despliegue en test)."
  type        = string

  validation {
    condition     = contains(["dev", "test"], var.ambiente)
    error_message = "El ambiente debe ser dev o test."
  }
}

variable "ubicacion" {
  description = "Región de Azure. East US 2 tiene todos los servicios de la capa gratuita para estudiantes."
  type        = string
  default     = "eastus2"
}

variable "sku_app_service" {
  description = "Plan de App Service. B1 es el más pequeño que permite Always On."
  type        = string
  default     = "B1"
}

variable "sql_admin_login" {
  description = "Nombre del grupo o usuario de Microsoft Entra ID que administra Azure SQL."
  type        = string
}

variable "sql_admin_object_id" {
  description = "Object ID de ese grupo o usuario en Microsoft Entra ID."
  type        = string
}

variable "etiquetas" {
  description = "Etiquetas comunes para costos y trazabilidad."
  type        = map(string)
  default = {
    proyecto = "KuboERP"
    curso    = "Ingenieria de Software II"
    sprint   = "2"
  }
}
