terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Estado remoto en una cuenta de almacenamiento de Azure. Se configura en GitHub Actions con
  # `terraform init -backend-config=...`; para validar sin Azure se usa `terraform init -backend=false`.
  backend "azurerm" {}
}

# La suscripción se toma de la variable de entorno ARM_SUBSCRIPTION_ID (GitHub Actions la recibe como secreto).
provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}
