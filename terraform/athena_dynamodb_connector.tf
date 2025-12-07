data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  athena_catalog_name  = "dynamo_db"
  glue_connection_name = "dynamo_db_with_glue"
}

resource "aws_serverlessapplicationrepository_cloudformation_stack" "athena_ddb_connector" {
  name             = "func_athena_dynamo"
  application_id   = "arn:aws:serverlessrepo:us-east-1:292517598671:applications/AthenaDynamoDBConnectorWithGlueConnection"
  semantic_version = "2025.43.1"
  capabilities     = ["CAPABILITY_IAM"]

  parameters = {
    AthenaCatalogName  = local.athena_catalog_name
    SpillBucket        = aws_s3_bucket.twitch_streams_utils_bucket.bucket
    GlueConnectionName = local.glue_connection_name
  }
}

resource "aws_lambda_permission" "athena_invoke_connector" {
  statement_id  = "AllowAthenaInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_serverlessapplicationrepository_cloudformation_stack.athena_ddb_connector.outputs["LambdaFunctionQualifiedArn"]
  principal     = "athena.amazonaws.com"
  source_arn    = "arn:aws:athena:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:workgroup/*"
}

resource "aws_athena_data_catalog" "dynamodb" {
  name = local.athena_catalog_name
  type = "LAMBDA"

  parameters = {
    function = aws_serverlessapplicationrepository_cloudformation_stack.athena_ddb_connector.outputs["LambdaFunctionQualifiedArn"]
  }
}
