output "region" {
  description = "AWS region"
  value       = var.region
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = var.cluster_name
}

output "efs" {
  value = module.eks.efs
}

output "rds_endpoint" {
  value = module.rds.rds_endpoint
}

output "s3_arn_raw" {
  value = module.s3.s3_bucket_arn_raw
}

output "s3_arn_staging" {
  value = module.s3.s3_bucket_arn_staging
}
