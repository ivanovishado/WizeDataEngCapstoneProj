output "s3_bucket_id_raw" {
    value = aws_s3_bucket.raw_layer.id
}
output "s3_bucket_arn_raw" {
    value = aws_s3_bucket.raw_layer.arn
}
output "s3_bucket_domain_name_raw" {
    value = aws_s3_bucket.raw_layer.bucket_domain_name
}
output "s3_hosted_zone_id_raw" {
    value = aws_s3_bucket.raw_layer.hosted_zone_id
}
output "s3_bucket_region_raw" {
    value = aws_s3_bucket.raw_layer.region
}

output "s3_bucket_id_staging" {
    value = aws_s3_bucket.staging_layer.id
}
output "s3_bucket_arn_staging" {
    value = aws_s3_bucket.staging_layer.arn
}
output "s3_bucket_domain_name_staging" {
    value = aws_s3_bucket.staging_layer.bucket_domain_name
}
output "s3_hosted_zone_id_staging" {
    value = aws_s3_bucket.staging_layer.hosted_zone_id
}
output "s3_bucket_region_staging" {
    value = aws_s3_bucket.staging_layer.region
}
