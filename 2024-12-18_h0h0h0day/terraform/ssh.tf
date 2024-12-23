# Generate a new private key
resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create temporary SSH key in DO
resource "digitalocean_ssh_key" "do_ssh_key" {
  name       = "mhack-h0h0-${var.H0H0_YEAR}"
  public_key = tls_private_key.ssh.public_key_openssh
}

# Store private key locally for Ansible to use
resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/../.secrets/ssh"
  file_permission = "0600"
}

# public key locally for Ansible to use
resource "local_sensitive_file" "public_key" {
  content         = tls_private_key.ssh.public_key_fingerprint_sha256
  filename        = "${path.module}/../.secrets/ssh.pub"
  file_permission = "0660"
}
