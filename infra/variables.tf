variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-084568db4383264d4"  # Ubuntu 22.04 LTS
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "ssh_access_cidr" {
  description = "CIDR block for SSH access (your IP address with /32)"
  type        = string
  default     = "0.0.0.0/32"  # Change this to your IP address in production
}

variable "key_name" {
  description = "Name of the SSH key pair to use for the EC2 instance"
  type        = string
  default     = "embrapa-viticulture-key"  # Change this to your key pair name
} 