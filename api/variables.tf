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

variable "aws_auth_file" {
    description = "AWS auth file"
    type        = string
}

variable "aws_auth_profile" {
    description = "AWS auth profile"
    type        = string
}
