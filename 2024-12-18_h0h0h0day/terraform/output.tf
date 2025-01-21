# Useful for quick SSH, see README.adoc
output "ctfd_ip" {
  value = digitalocean_droplet.ctfd.ipv4_address
}
output "challenge_ip" {
  value = digitalocean_droplet.challenge.ipv4_address
}
