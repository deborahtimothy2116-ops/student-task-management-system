# ==============================================================================
# Infrastructure as Code (IaC) - Terraform Configuration for EduTask
# Unit-V Supporting Activity: Course 231CS523
# Provisions automated containerized deployment using Docker Provider
# ==============================================================================

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

# Isolated Bridge Network
resource "docker_network" "edutask_network" {
  name = "edutask_iac_network"
}

# Image definition
resource "docker_image" "edutask_image" {
  name         = "edutask:${var.app_image_tag}"
  keep_locally = true
}

# Production Container Instance
resource "docker_container" "edutask_container" {
  name  = var.container_name
  image = docker_image.edutask_image.image_id
  
  restart = "always"

  ports {
    internal = 8000
    external = var.app_port
  }

  env = [
    "APP_ENV=${var.environment}",
    "PORT=8000"
  ]

  networks_advanced {
    name = docker_network.edutask_network.name
  }

  healthcheck {
    test     = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"]
    interval = "30s"
    timeout  = "5s"
    retries  = 3
  }
}

# Outputs
output "application_url" {
  description = "Access URL for EduTask application"
  value       = "http://localhost:${var.app_port}"
}

output "container_id" {
  description = "Docker Container ID of the deployed service"
  value       = docker_container.edutask_container.id
}
