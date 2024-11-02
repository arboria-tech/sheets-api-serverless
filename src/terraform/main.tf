provider "aws" {
  region = "us-east-1"
}

# ----------------------------------------
# IAM Roles e Permissões
# ----------------------------------------

# Cria a role IAM para as Lambdas
resource "aws_iam_role" "lambda_role" {
  name = "lambda_sheets_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Effect = "Allow"
      Sid    = ""
    }]
  })
}

# Anexa políticas gerenciadas amplas à role
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name

  depends_on = [aws_iam_role.lambda_role]
}

# ----------------------------------------
# Criação de Lambda Layers
# ----------------------------------------

# Cria a Lambda Layer
resource "aws_lambda_layer_version" "google_sheets_layer" {
  filename            = "./deployments/google_sheets_layer.zip"
  layer_name          = "extract-layer"
  compatible_runtimes = ["python3.11"]
  source_code_hash    = filebase64sha256("./deployments/google_sheets_layer.zip")
}

# ----------------------------------------
# Criação de Lambdas
# ----------------------------------------

# Lambda de get sheets events
module "lambda_get_sheets_all_records" {
  source        = "./modules/lambda"
  function_name = "get_sheets_all_records"
  role_arn      = aws_iam_role.lambda_role.arn
  zip_file      = "./deployments/get_sheets_all_records.zip"
  layers = [
    aws_lambda_layer_version.google_sheets_layer.arn
  ]
  environment_variables = {}
  api_gw_execution_arn = aws_apigatewayv2_api.http_api.execution_arn
}

# ----------------------------------------
# API Gateway
# ----------------------------------------

# Cria o API Gateway
resource "aws_apigatewayv2_api" "http_api" {
  name          = "http-api-google-sheets"
  protocol_type = "HTTP"
}

# Stage da API
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

# Configura os endpoints do API Gateway
module "api_gateway_get_sheets_all_records" {
  source            = "./modules/api_gateway"
  api_id            = aws_apigatewayv2_api.http_api.id
  method            = "POST"
  path              = "/get_sheets_all_records"
  lambda_invoke_arn = module.lambda_get_sheets_all_records.lambda_invoke_arn
}
