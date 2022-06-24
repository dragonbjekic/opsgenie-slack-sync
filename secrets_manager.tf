resource "aws_secretsmanager_secret" "secret" {
  name = var.secret_name

  tags = var.tags
}

resource "aws_secretsmanager_secret_policy" "secret" {
  secret_arn = aws_secretsmanager_secret.secret.arn

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetValue",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_iam_role.role.arn}"
      },
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "*"
    }
  ]
}
POLICY

  depends_on = [
    aws_iam_role.role
  ]
}

output "secret_arn" {
  description = "Arn of secret with API keys"
  value       = aws_secretsmanager_secret.secret.arn
}
