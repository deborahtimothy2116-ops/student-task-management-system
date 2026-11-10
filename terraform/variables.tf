variable "app_port" {
  description = "Host port exposed for EduTask web application"
  type        = number
  default     = 8000
}

variable "container_name" {
  description = "Name of the deployed Docker container"
  type        = string
  default     = "edutask_prod_instance"
}

variable "environment" {
  description = "Deployment environment (development, staging, production)"
  type        = string
  default     = "production"
}

variable "app_image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}
