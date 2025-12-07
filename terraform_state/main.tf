terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}

provider "aws" {
  region = "sa-east-1"
}

locals {
  state_bucket = "tfstate-twitch-state-bucket"
  lock_table   = "tfstate-locks"
}

resource "aws_s3_bucket" "tf_bucket_state_twitch" {
  bucket = local.state_bucket
  lifecycle { prevent_destroy = true }
}

resource "aws_dynamodb_table" "locks" {
  name         = local.lock_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  lifecycle { prevent_destroy = true }
}
