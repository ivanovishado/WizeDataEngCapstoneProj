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

output "s3_id_raw" {
  value = module.s3.s3_bucket_id_raw
}

output "s3_id_staging" {
  value = module.s3.s3_bucket_id_staging
}

output "s3_id_spark" {
  value = module.s3.s3_bucket_id_spark
}

output "subnet_ids" {
  value = module.networking.private_subnets_ids
}
