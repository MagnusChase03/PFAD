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

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = var.aws_lambda_layer_file
  layer_name = var.aws_lambda_layer_name

  compatible_runtimes = ["python3.12"]
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

resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = var.aws_lambda_function_name
  role          = aws_iam_role.aws_lambda_iam.arn
  handler       = "main.handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.12"
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
}
