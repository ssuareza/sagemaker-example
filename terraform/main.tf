variable "bucket_name" {
  type = string
}

resource "aws_s3_bucket" "model_bucket" {
  bucket = var.bucket_name
}

output "bucket_name" {
  value = aws_s3_bucket.model_bucket.bucket
}
