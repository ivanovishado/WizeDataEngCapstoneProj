provider "aws" {
  region = var.region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.0"
    }

    dotenv = {
      source  = "jrhouston/dotenv"
      version = "~> 1.0"
    }
  }
}
