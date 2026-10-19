output "instance_id" {
  value = aws_instance.prueba.id
}

output "lambda_name" {
  value = aws_lambda_function.auto_stop.function_name
}