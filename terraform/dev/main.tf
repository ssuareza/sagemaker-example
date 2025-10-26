module "s3" {
  source      = "../modules/s3_bucket"
  bucket_name = "my-model-dev-bucket"
}
