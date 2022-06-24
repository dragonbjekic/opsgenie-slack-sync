variable "tags" {
  type = map(any)
}

variable "secret_name" {
  type = string
}

variable "lambda_location" {
  type = string
}

variable "lambda_role_name" {
  type = string
}
variable "function_name" {
  type = string
}
variable "function_handler" {
  type = string
}
variable "runtime" {
  type = string
}

variable "schedule_expression" {
  type = string
}
