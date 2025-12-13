# Generate a new private key
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
# Store private key locally for Ansible to use
resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/../.secrets/ssh"
  file_permission = "0600"
}

# public key locally for Ansible to use
resource "local_sensitive_file" "public_key" {
  content         = tls_private_key.ssh.public_key_openssh
  filename        = "${path.module}/../.secrets/ssh.pub"
  file_permission = "0660"
}

# Read other authorized keys
locals {
  ssh_extra_keys = compact(split("\n", file("../.secrets/authorized_keys")))
}
