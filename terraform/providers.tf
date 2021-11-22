provider "aws" {
  region = var.region
}

provider "airflow" {
  base_endpoint = module.eks.efs
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.0"
    }

    airflow = {
      source  = "houqp/airflow"
      version = "0.2.1"
    }

    dotenv = {
      source  = "jrhouston/dotenv"
      version = "~> 1.0"
    }
  }
}
