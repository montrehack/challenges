resource "incus_instance" "ctfd" {
  name   = "h0h0h0-${var.H0H0_YEAR}-ctfd"
  project = data.incus_project.montrehack.name

  image  = "images:ubuntu/24.04/cloud"
  type = "virtual-machine"
  profiles = [data.incus_profile.default.name]

  config = {
      "cloud-init.user-data" = <<EOF
#cloud-config
package_update: true
packages:
  - openssh-server
  - sudo

ssh_genkeytypes: ['rsa', 'ecdsa', 'ed25519']

runcmd:
  - [ sh, -c, "test -f /etc/ssh/ssh_host_rsa_key || ssh-keygen -A" ]
  - systemctl enable ssh
  - systemctl start ssh

users:
  - name: montrehack
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    ssh_authorized_keys: ${jsonencode(concat([tls_private_key.ssh.public_key_openssh], local.ssh_extra_keys))}
EOF
  }
}

resource "incus_network_forward" "ctfd_forward_v4" {
  network        = data.incus_network.default.name
  project        = data.incus_project.montrehack.name
  listen_address = var.CTFD_EXTERNAL_IPV4

  config = {
    target_address = incus_instance.ctfd.ipv4_address
  }
}

resource "incus_network_forward" "ctfd_forward_v6" {
  network        = data.incus_network.default.name
  project        = data.incus_project.montrehack.name
  listen_address = var.CTFD_EXTERNAL_IPV6

  config = {
    target_address = incus_instance.ctfd.ipv6_address
  }
}

# DNS
resource "cloudflare_record" "ctfd_dns_ipv4" {
  zone_id = data.cloudflare_zone.montrehack.id
  name    = "h0h0h0day"
  type    = "A"
  content = var.CTFD_EXTERNAL_IPV4
  ttl     = 3600
  proxied = false
}

resource "cloudflare_record" "ctfd_dns_ipv6" {
  zone_id = data.cloudflare_zone.montrehack.id
  name    = "h0h0h0day"
  type    = "AAAA"
  content = var.CHALLENGE_EXTERNAL_IPV6
  ttl     = 3600
  proxied = false
}
