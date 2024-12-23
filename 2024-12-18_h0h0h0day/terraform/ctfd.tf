resource "digitalocean_droplet" "ctfd" {
  image    = "ubuntu-22-04-x64"
  name     = "h0h0h0day-${var.H0H0_YEAR}-ctfd"
  region   = "tor1"
  ipv6     = true
  vpc_uuid = digitalocean_vpc.ctfd.id
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
    #agent = true
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

# Generate Ansible inventory file
resource "local_file" "ansible_inventory" {
  content = templatefile("ansible-inventory.tmpl",
    {
      ctfd_ip = digitalocean_droplet.ctfd.ipv4_address
      ctfd_sshprivkey = local_sensitive_file.private_key.filename
    }
  )
  filename = "../ansible/inventory.yml"
  file_permission = "0660"
}

# Event year
variable "H0H0_YEAR" {
  type = string
}

# Section below handle creating a random vpc per droplet instance
resource "random_pet" "vpc_name" {}

resource "digitalocean_vpc" "ctfd" {
  name   = "h0h0h0-${random_pet.vpc_name.id}"
  region = "tor1"
}
