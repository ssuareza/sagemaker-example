resource "aws_s3_bucket" "sagemaker_example" {
  bucket = "sagemaker-example-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_acl" "sagemaker_example_acl" {
  bucket = aws_s3_bucket.sagemaker_example.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "sagemaker_example_public_access_block" {
  bucket = aws_s3_bucket.sagemaker_example.id

  block_public_acls       = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# random id to create a bucket name
resource "random_id" "suffix" {
  byte_length = 4
}
