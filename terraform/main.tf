provider "aws" {
  region = var.aws_region
}

resource "aws_ecr_repository" "ai_repo" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"
}

resource "aws_apprunner_service" "ai_service" {
  service_name = var.project_name

  source_configuration {
    image_repository {
      image_configuration {
        port = "8000"
      }
      image_identifier      = "${aws_ecr_repository.ai_repo.repository_url}:latest"
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = true
  }
}