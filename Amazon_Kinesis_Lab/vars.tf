variable "cidr" {
  description = "(Optional) The IPv4 CIDR block for the VPC. CIDR can be explicitly set or it can be derived from IPAM using `ipv4_netmask_length` & `ipv4_ipam_pool_id`"
  type        = string
  default     = "172.16.0.0/16"
}

variable "vpcname" {
  description = "vpc name you can bypass another value or let it pass the default"
  type        = string
  default     = "dea-vpc"
}

variable "privatesubnet" {
  description = "Private subnet"
  type        = string
  default     = "172.16.0.96/28"
}

variable "publicsubnet" {
  description = "Public subnet"
  type        = string
  default     = "172.16.0.112/28"
}

variable "gwname" {
  description = "gateway name"
  type        = string
  default     = "dea-gw"
}


variable "instancetype" {
  description = "EC2 instance type"
  default = "t2.micro"
 }

variable "ami_id" {
  description = "AMI ID"
  default = "ami-0bbd3f89449af0b30"
}

variable "key_name" {
    default = "dea-key"
  }


variable "dbname" {
  description = "database instance name"
  type        = string
  default     = "deadb"
  
}


variable "dbadmin" {
  description = "Database admin name"
  type        = string
  default     = "dbadmin"
}


variable "password" {
  description = "database password"
  type        = string
  default     = "Password123"
}  



variable "instance_security_group_name" {
  description = "The name of the security group for the EC2 Instances"
  type        = string
  default     = "dea-instance-sg"
}

variable "db_security_group_name" {
  description = "The name of the security group for the EC2 Instances"
  type        = string
  default     = "dea-db-instance"
}

variable "ssh" {
  type = number
  default = 22
}

variable "mysql" {
  type = number
  default = 3306
}



variable "dbidentifier" {
  type = string
  default = "deainstance"
  }
