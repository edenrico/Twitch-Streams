terraform {
  backend "s3" {
    bucket         = "tfstate-twitch-state-bucket"
    key            = "twitch-streams/terraform.tfstate"
    region         = "sa-east-1"
    dynamodb_table = "tfstate-locks"
    encrypt        = true
  }
}
