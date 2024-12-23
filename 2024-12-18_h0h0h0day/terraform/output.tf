# Useful for quick SSH, see README.adoc
output "ctfd_ip" {
  value = digitalocean_droplet.ctfd.ipv4_address
}
