terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.5"
    }
  }
}

provider "aws" {
  region = "sa-east-1"
}

locals {
  project_name          = "twitch-streams"
  bucket_raw_silver     = "twitch-streams-s3"
  bucket_utils          = "datalake-utils-twitch-streams"
  bucket_athena_logs    = "athena-logs-twitch-streams"
  sqs_queue_name        = "Twitch-real-time-sqs"
  sqs_dlq_name          = "Twitch-real-time-DLQ"
  dynamodb_table_name   = "tbl_live_streams"
  lambda_realtime_name  = "Twitch-sqs-dynamodb-lambda"
  glue_role_name        = "AWSGlueServiceRole-twitch-streams"
  glue_job_silver_name  = "silver_glue"
  glue_job_gold_name    = "gold_glue"
  glue_db_raw           = "db_raw"
  glue_db_silver        = "db_silver"
  athena_workgroup_name = "athena_twitch_streams"
  athena_query_results  = "s3://${local.bucket_athena_logs}/athena_bronze_raw_logs/"
}
