data "aws_iam_policy_document" "glue_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "glue_role" {
  name               = local.glue_role_name
  assume_role_policy = data.aws_iam_policy_document.glue_assume_role.json
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

data "aws_iam_policy_document" "glue_extra_policy" {
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
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.twitch_streams_bucket.arn,
      "${aws_s3_bucket.twitch_streams_bucket.arn}/*",
      aws_s3_bucket.twitch_streams_utils_bucket.arn,
      "${aws_s3_bucket.twitch_streams_utils_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "glue_extra" {
  name   = "${local.glue_role_name}-extra"
  role   = aws_iam_role.glue_role.id
  policy = data.aws_iam_policy_document.glue_extra_policy.json
}

# Scripts enviados para o bucket principal
resource "aws_s3_object" "silver_glue_script" {
  bucket       = aws_s3_bucket.twitch_streams_bucket.id
  key          = "scripts/silver_glue.py"
  source       = "${path.module}/../stages/silver/silver_glue.py"
  content_type = "text/x-python"
  etag         = filemd5("${path.module}/../stages/silver/silver_glue.py")
}

resource "aws_s3_object" "gold_glue_script" {
  bucket       = aws_s3_bucket.twitch_streams_bucket.id
  key          = "scripts/gold_glue.py"
  source       = "${path.module}/../stages/gold/gold_glue.py"
  content_type = "text/x-python"
  etag         = filemd5("${path.module}/../stages/gold/gold_glue.py")
}

# Catálogos
resource "aws_glue_catalog_database" "raw" {
  name = local.glue_db_raw
}

resource "aws_glue_catalog_database" "silver" {
  name = local.glue_db_silver
}

# Crawlers
resource "aws_glue_crawler" "raw" {
  name         = "crawler-raw"
  role         = aws_iam_role.glue_role.arn
  database_name = aws_glue_catalog_database.raw.name

  s3_target {
    path = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/raw/"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }
}

resource "aws_glue_crawler" "silver" {
  name          = "crawler-silver"
  role          = aws_iam_role.glue_role.arn
  database_name = aws_glue_catalog_database.silver.name

  s3_target {
    path = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/silver/"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }
}

# Jobs
resource "aws_glue_job" "silver_job" {
  name     = local.glue_job_silver_name
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/scripts/silver_glue.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"          = "python"
    "--TempDir"               = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/glue_logs/"
    "--enable-continuous-cloudwatch-log" = "true"
  }

  glue_version       = "4.0"
  worker_type        = "G.1X"
  number_of_workers  = 2
  timeout            = 10
  max_retries        = 0
  execution_property { max_concurrent_runs = 1 }

  depends_on = [
    aws_s3_object.silver_glue_script,
    aws_iam_role_policy.glue_extra
  ]
}

resource "aws_glue_job" "gold_job" {
  name     = local.glue_job_gold_name
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/scripts/gold_glue.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"          = "python"
    "--TempDir"               = "s3://${aws_s3_bucket.twitch_streams_bucket.bucket}/glue_logs/"
    "--enable-continuous-cloudwatch-log" = "true"
  }

  glue_version       = "4.0"
  worker_type        = "G.1X"
  number_of_workers  = 2
  timeout            = 10
  max_retries        = 0
  execution_property { max_concurrent_runs = 1 }

  depends_on = [
    aws_s3_object.gold_glue_script,
    aws_iam_role_policy.glue_extra
  ]
}
