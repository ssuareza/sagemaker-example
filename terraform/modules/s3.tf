resource "aws_s3_bucket" "model_bucket" {
  bucket = var.bucket_name
  acl    = "private"
}

output "bucket_name" {
  value = aws_s3_bucket.model_bucket.bucket
}

