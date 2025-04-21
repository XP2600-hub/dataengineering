resource "aws_vpc" "dea" {

cidr_block = var.cidr

# cidr block iteration found in the terraform.tfvars file

tags = {

Name = var.vpcname
}
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {

    most_recent = true

    filter {
        name   = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
    }

    filter {
        name = "virtualization-type"
        values = ["hvm"]
    }

    owners = ["099720109477"]
}


resource "aws_subnet" "privatesubnet" {  
   vpc_id = aws_vpc.dea.id
   availability_zone = data.aws_availability_zones.available.names[0]
   cidr_block = var.privatesubnet
 }

resource "aws_subnet" "publicsubnet" {  
   vpc_id = aws_vpc.dea.id
   availability_zone = data.aws_availability_zones.available.names[1]
   cidr_block = var.publicsubnet
 }

 resource "aws_internet_gateway" "gw" {

vpc_id =  aws_vpc.dea.id
tags = {
  Name = var.gwname
  }

}

# Create EIP for the IGW

resource "aws_eip" "myEIP" {
   vpc   = true
 }

 # Creating RT for Public Subnet
 resource "aws_route_table" "publRT" {
  vpc_id =  aws_vpc.dea.id
     route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
     }
 }
#Associating the Public RT with the Public Subnets
resource "aws_route_table_association" "PubRTAss" {
subnet_id = aws_subnet.publicsubnet.id
route_table_id = aws_route_table.publRT.id
}


resource "tls_private_key" "deatls" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "deagenkey" {
  key_name   = var.key_name
  public_key = tls_private_key.deatls.public_key_openssh
}


resource "aws_instance" "dea-jumpbox" {
  count = 1
  ami = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.micro"
  key_name = aws_key_pair.deagenkey.key_name
  vpc_security_group_ids = [aws_security_group.dea-instance.id]
  subnet_id = aws_subnet.publicsubnet.id
  associate_public_ip_address = true
  tags = { Name = "dea-jumpbox"
  } 

}

resource "aws_security_group" "dea-instance" {
  name = var.instance_security_group_name
  vpc_id      = aws_vpc.dea.id
  ingress {
    from_port   = var.ssh
    to_port     = var.ssh
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
      }
      egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
      }
}

resource "aws_security_group" "dea-db-instance" {
  name = var.db_security_group_name
  vpc_id      = aws_vpc.dea.id
  ingress {
    from_port   = var.mysql
    to_port     = var.mysql
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
      }
      egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
      }
}


resource "aws_db_subnet_group" "dea_db_subnet_group" {
  name       = "my-db-subnet-group"
  subnet_ids = [aws_subnet.privatesubnet.id, aws_subnet.publicsubnet.id]

  tags = {
    Name = "dea DB Subnet Group"
  }
}


resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = var.dbname
  identifier = var.dbidentifier
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = var.dbadmin
  password             = var.password
  parameter_group_name = "default.mysql5.7"
  db_subnet_group_name    = aws_db_subnet_group.dea_db_subnet_group.name
  skip_final_snapshot  = true
  multi_az = false
  vpc_security_group_ids = [aws_security_group.dea-db-instance.id]
}



