output "jumpbox_public_ips" {
  value = aws_instance.dea-jumpbox[*].public_ip
  description = "Public IP addresses of the DEA jumpbox instances"
}

output "dea-key" {
  value     = tls_private_key.deatls.private_key_pem
  sensitive = true
}

output "dbinstance-address" {
  value = aws_db_instance.default.address
  description = "database instance address"
}