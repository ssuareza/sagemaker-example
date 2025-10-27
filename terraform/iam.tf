# 1. Create the IAM role
resource "aws_iam_role" "sagemaker_example" {
  name = "sagemaker-example"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_full_access" {
  role       = aws_iam_role.sagemaker_example.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.sagemaker_example.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

output "sagemaker_role_arn" {
  value = aws_iam_role.sagemaker_example.arn
}
