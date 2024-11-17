variable "aws_region" {
    description = "AWS region"
    type        = string
    default     = "us-east-1"
}

variable "aws_bucket_name" {
    description = "AWS bucket name"
    type        = string
    default     = "s3-hackutd-2024-bucket"
}

variable "aws_lambda_function_name" {
    description = "AWS lambda function name"
    type        = string
    default     = "lambda-hackutd-2024-function"
}

variable "aws_auth_file" {
    description = "AWS auth file"
    type        = string
}

variable "aws_auth_profile" {
    description = "AWS auth profile"
    type        = string
}
