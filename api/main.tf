terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "5.76.0"
        }
    }
}

provider "aws" {
    region = var.aws_region
    shared_config_files      = [var.aws_auth_file]
    shared_credentials_files = [var.aws_auth_file]
    profile                  = var.aws_auth_profile
}

resource "aws_s3_bucket" "aws_bucket" {
    bucket = var.aws_bucket_name
}

data "aws_iam_policy_document" "aws_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "aws_lambda_iam" {
  name               = "aws_lambda_iam"
  assume_role_policy = data.aws_iam_policy_document.aws_assume_role.json
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "main.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "aws_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = var.aws_lambda_function_name
  role          = aws_iam_role.aws_lambda_iam.arn
  handler       = "main.handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.12"

  environment {
    variables = {
      bucket = var.aws_bucket_name
    }
  }
}

data "aws_iam_policy_document" "lambda_perms" {
  statement {
    effect = "Allow"

    actions = [
      "s3:*",
      "logs:*"
    ]

    resources = ["arn:aws:s3:::*", "arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_perms" {
  name        = "lambda_perms"
  path        = "/"
  description = "IAM policy for accessing s3 from a lambda"
  policy      = data.aws_iam_policy_document.lambda_perms.json
}

resource "aws_iam_role_policy_attachment" "lambda_perms" {
  role       = aws_iam_role.aws_lambda_iam.name
  policy_arn = aws_iam_policy.lambda_perms.arn
}

resource "aws_lambda_function_url" "lambda_url" {
  function_name      = aws_lambda_function.aws_lambda.function_name
  authorization_type = "NONE"
}
