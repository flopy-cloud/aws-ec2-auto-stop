variable "region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

# EventBridge usa hora UTC. Argentina es UTC-3.
variable "stop_cron" {
  description = "Apagar a las 22:00 hora Argentina (01:00 UTC)"
  type        = string
  default     = "cron(0 1 * * ? *)"
}

variable "start_cron" {
  description = "Prender a las 08:00 hora Argentina (11:00 UTC)"
  type        = string
  default     = "cron(0 11 * * ? *)"
}