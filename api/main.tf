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
