# Buckets já existentes (ajuste para importar antes de aplicar)
resource "aws_s3_bucket" "twitch_streams_bucket" {
  bucket = "twitch-streams-s3"

  tags = {
    Projeto  = "Twitch Streams"
    Ambiente = "Producao"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket" "twitch_streams_utils_bucket" {
  bucket = "datalake-utils-twitch-streams"

  tags = {
    Projeto  = "Twitch Streams"
    Ambiente = "Producao"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Bucket de logs do Athena (existente)
resource "aws_s3_bucket" "athena_logs_bucket" {
  bucket = "athena-logs-twitch-streams"

  tags = {
    Projeto  = "Twitch Streams"
    Ambiente = "Producao"
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Pastas no bucket principal
resource "aws_s3_object" "raw_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "raw/"
  content = " "
}

resource "aws_s3_object" "silver_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "silver/"
  content = " "
}

resource "aws_s3_object" "gold_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "gold/"
  content = " "
}

resource "aws_s3_object" "scripts_folder" {
  bucket  = aws_s3_bucket.twitch_streams_bucket.id
  key     = "scripts/"
  content = " "
}

# Logs Glue e Athena no bucket de utilidades
resource "aws_s3_object" "glue_logs_folder" {
  bucket  = aws_s3_bucket.twitch_streams_utils_bucket.id
  key     = "glue_logs/"
  content = " "
}

resource "aws_s3_object" "athena_logs_folder" {
  bucket  = aws_s3_bucket.athena_logs_bucket.id
  key     = "athena_bronze_raw_logs/"
  content = " "
}
