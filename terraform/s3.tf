# Twitch bucket
resource "aws_s3_bucket" "twitch_streams_bucket" {
  bucket = "twitch_streams_s3"
  tags = {
    Projeto = "Twitch Streams"
    Ambiente = "Producao" # ou "Desenvolvimento"
  }
}

# raw folder 
resource "aws_s3_object" "raw_folder" {
  bucket = aws_s3_bucket.twitch_streams_bucket.id
  key = "raw/"
  content = " "
}

# silver folder
resource "aws_s3_object" "silver_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "silver/"
  content = " "
}

# scripts folder
resource "aws_s3_object" "scripts_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "scripts/"
  content = " "
}
