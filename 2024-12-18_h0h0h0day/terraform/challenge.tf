resource "digitalocean_droplet" "challenge" {
  image    = "ubuntu-24-04-x64"
  name     = "h0h0h0day-${var.H0H0_YEAR}-challenge"
  region   = "tor1"
  ipv6     = true
  vpc_uuid = digitalocean_vpc.challenge.id
  # initial size (smallest cpu-optimized)
  size     = "s-2vcpu-4gb"
  # production size
  #size     = "c-16-intel"
  resize_disk = false
  ssh_keys = [digitalocean_ssh_key.do_ssh_key.fingerprint]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    private_key = tls_private_key.ssh.private_key_pem
    timeout = "2m"
  }

  # Wait until instance responds to SSH before triggering next actions
  provisioner "remote-exec" {
    inline = [
      "until [ -f /var/lib/cloud/instance/boot-finished ]; do sleep 1; done",
      "apt -y update"
    ]
  }
}

# Section below handle creating a random vpc per droplet instance
resource "random_pet" "vpc_name_challenge" {}

resource "digitalocean_vpc" "challenge" {
  name   = "h0h0h0-${random_pet.vpc_name_challenge.id}"
  region = "tor1"
}

# DNS
resource "cloudflare_record" "challenge_dns_ipv4" {
  zone_id = data.cloudflare_zone.montrehack.id
  name    = "challenges"
  type    = "A"
  content = digitalocean_droplet.challenge.ipv4_address
  ttl     = 3600
  proxied = false
}

# Disabled due to digitalocean DockerHub issue (see README.adoc)
#resource "cloudflare_record" "challenge_dns_ipv6" {
#  zone_id = data.cloudflare_zone.montrehack.id
#  name    = "challenges"
#  type    = "AAAA"
#  content = digitalocean_droplet.challenge.ipv6_address
#  ttl     = 3600
#  proxied = false
#}
