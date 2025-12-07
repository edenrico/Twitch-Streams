data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_sqs_queue" "realtime_dlq" {
  name                        = local.sqs_dlq_name
  message_retention_seconds   = 1209600
  visibility_timeout_seconds  = 30
  receive_wait_time_seconds   = 10
  sqs_managed_sse_enabled     = true
}

resource "aws_sqs_queue" "realtime" {
  name                        = local.sqs_queue_name
  visibility_timeout_seconds  = 120
  receive_wait_time_seconds   = 10
  sqs_managed_sse_enabled     = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.realtime_dlq.arn
    maxReceiveCount     = 5
  })
}

resource "aws_dynamodb_table" "streams" {
  name         = local.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "nome_streamer"
  range_key    = "timestamp"

  attribute {
    name = "nome_streamer"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Projeto  = "Twitch Streams"
    Ambiente = "Producao"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role" "lambda_realtime_role" {
  name               = "${local.lambda_realtime_name}-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_realtime_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"]
  }

  statement {
    actions = [
      "dynamodb:BatchWriteItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem"
    ]
    resources = [aws_dynamodb_table.streams.arn]
  }

  statement {
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ChangeMessageVisibility"
    ]
    resources = [aws_sqs_queue.realtime.arn]
  }
}

resource "aws_iam_role_policy" "lambda_realtime_inline" {
  name   = "${local.lambda_realtime_name}-policy"
  role   = aws_iam_role.lambda_realtime_role.id
  policy = data.aws_iam_policy_document.lambda_realtime_policy.json
}

data "archive_file" "lambda_realtime_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../streaming_pipeline/lambda_sqs_to_timestream"
  output_path = "${path.module}/lambda_sqs_to_dynamodb.zip"
}

resource "aws_lambda_function" "realtime_consumer" {
  function_name = local.lambda_realtime_name
  role          = aws_iam_role.lambda_realtime_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.13"

  filename         = data.archive_file.lambda_realtime_zip.output_path
  source_code_hash = data.archive_file.lambda_realtime_zip.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = local.dynamodb_table_name
    }
  }

  depends_on = [aws_iam_role_policy.lambda_realtime_inline]
}

resource "aws_lambda_event_source_mapping" "sqs_to_lambda" {
  event_source_arn = aws_sqs_queue.realtime.arn
  function_name    = aws_lambda_function.realtime_consumer.arn
  batch_size       = 10
  enabled          = true
}
