resource "aws_ecr_repository" "sagemaker_example" {
  name = "sagemaker-example"
}

resource "aws_s3_bucket" "sagemaker_example" {
  bucket = "sagemaker-example"
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
