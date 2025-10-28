resource "aws_s3_bucket" "sagemaker_example" {
  bucket = "sagemaker-example-${random_id.suffix.hex}"
}

# random id to create a bucket name
resource "random_id" "suffix" {
  byte_length = 4
}

# output
output "sagemaker_bucket_name" {
  value = aws_s3_bucket.sagemaker_example.id
}
