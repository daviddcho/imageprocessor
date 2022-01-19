variable "cidr_vpc" {
  description = "CIDR block for the VPC"
  default     = "10.1.0.0/16"
}

variable "cidr_subnet" {
  description = "CIDR block for the subnet"
  default     = "10.1.0.0/24"
}

variable "environment_tag" {
  description = "Environment tag"
  default     = "Learn"
}

variable "instance_name" {
  description = "Value of the Name tag for EC2 instance"
  type        = string
  default     = "TestCloudInit"
}

variable "bucket_name" {
  description = "Name of S3 bucket"
  type        = string
  default     = "thisisatestingbucket123"
}

variable "bucket_acl" {
  description = "Access control list (ACL) of S3 bucket"
  type        = string
  default     = "private"
}
