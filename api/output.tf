output "aws_function_url" {
    value       = aws_lambda_function_url.lambda_url.function_url
    description = "The AWS Lambda endpoint"
}
