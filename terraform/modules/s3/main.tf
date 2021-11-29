resource "aws_s3_bucket" "raw_layer" {
  bucket_prefix = var.bucket_prefix
  acl           = "public-read-write"

  versioning {
    enabled = var.versioning
  }

  tags = {
    Name = "s3-data-bootcamp"
  }
}

resource "aws_s3_bucket" "staging_layer" {
  bucket_prefix = var.bucket_prefix
  acl           = "public-read-write"

  versioning {
    enabled = var.versioning
  }

  tags = {
    Name = "s3-data-bootcamp"
  }
}

resource "aws_s3_bucket" "spark_jobs" {
  bucket_prefix = var.bucket_prefix
  acl           = "public-read-write"

  versioning {
    enabled = var.versioning
  }

  tags = {
    Name = "s3-data-bootcamp"
  }
}
