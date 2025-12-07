locals {
  alerts_topic_name  = "sqs-alerts"
  alerts_email       = "aecesani@gmail.com"
  dlq_alarm_name     = "DLQ ALARM"
}

resource "aws_sns_topic" "sqs_alerts" {
  name = local.alerts_topic_name
}

resource "aws_sns_topic_subscription" "sqs_alerts_email" {
  topic_arn = aws_sns_topic.sqs_alerts.arn
  protocol  = "email"
  endpoint  = local.alerts_email
}

resource "aws_cloudwatch_metric_alarm" "sqs_dlq_depth" {
  alarm_name          = local.dlq_alarm_name
  alarm_description   = "Alert when DLQ has visible messages"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  threshold           = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Sum"

  dimensions = {
    QueueName = local.sqs_dlq_name
  }

  alarm_actions = [aws_sns_topic.sqs_alerts.arn]
  ok_actions    = [aws_sns_topic.sqs_alerts.arn]
}
