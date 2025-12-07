resource "aws_athena_workgroup" "twitch_streams" {
  name = local.athena_workgroup_name

  configuration {
    enforce_workgroup_configuration = false
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = local.athena_query_results
    }
  }

  tags = {
    Projeto  = "Twitch Streams"
    Ambiente = "Producao"
  }
}
