resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/24"
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.0/25"
}

resource "aws_subnet" "secondary" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.0.128/25"
}

module "airflow" {
  source = "datarootsio/ecs-airflow/aws"

  resource_prefix = "my-awsm-company"
  resource_suffix = "prod" # should go to env file

  vpc_id            = aws_vpc.main.id
  public_subnet_ids = [aws_subnet.main.id, aws_subnet.secondary.id]

  region = "us-east-2"

  airflow_executor = "Sequential"
  airflow_variables = {
    AIRFLOW__WEBSERVER__NAVBAR_COLOR : "#e27d60"
  }

  use_https = false
}
