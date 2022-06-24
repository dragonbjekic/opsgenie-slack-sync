resource "aws_iam_role" "role" {
  name               = var.lambda_role_name
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "role" {
  role       = aws_iam_role.role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.lambda_location
  output_path = "./lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  function_name    = var.function_name
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role = aws_iam_role.role.arn

  handler = var.function_handler
  runtime = var.runtime

  description = "update slack groups for current oncall rotation"
  timeout     = "180"

  environment {
    variables = {
      "SECRET_ARN" = aws_secretsmanager_secret.secret.arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.role,
    aws_secretsmanager_secret.secret
  ]
  provisioner "local-exec" {
    command = "rm lambda.zip"
  }

  tags = var.tags
}
