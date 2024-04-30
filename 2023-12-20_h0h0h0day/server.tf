resource "digitalocean_droplet" "ctfd" {
  image    = "ubuntu-22-04-x64"
  name     = "montrehack-h0h0h0day-2023"
  region   = "tor1"
  ipv6     = true
  vpc_uuid = digitalocean_vpc.server.id
  # initial size (smallest cpu-optimized)
  size     = "s-2vcpu-4gb"
  # production size
  #size     = "c-16-intel"
  resize_disk = false
  ssh_keys = [data.digitalocean_ssh_key.server.fingerprint]

  connection {
    host = self.ipv4_address
    user = "root"
    type = "ssh"
    agent = true
    #private_key = file(var.SSH_KEY_FILE)
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

resource "null_resource" "run-ansible-ctfd" {
  depends_on = [
    digitalocean_droplet.ctfd
  ]
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ../lib/ext/terraform.py ansible/server.yml"
  }
  triggers = {
    #always = timestamp()
    revision = "1"
  }
}

# Ansible provider for terrraform
resource "ansible_host" "ctfd" {
  count              = 1
  inventory_hostname = "ctfd"
  vars = {
    ansible_user = "root"
    ansible_host = digitalocean_droplet.ctfd.ipv4_address
    ansible_ssh_private_key_file = var.SSH_KEY_FILE
    ansible_python_interpreter = "/usr/bin/python3"
  }
}

# SSH keyname passed as an environment variable
variable "DO_SSH_KEY_NAME" {
  type = string
}
data "digitalocean_ssh_key" "server" {
  name = var.DO_SSH_KEY_NAME
}
# SSH keyfile passed as an environment variable
variable "SSH_KEY_FILE" {
  type = string
}

# Section below handle creating a random vpc per droplet instance
resource "random_pet" "vpc_name" {}

resource "digitalocean_vpc" "server" {
  name   = "honeynet-vpc-${random_pet.vpc_name.id}"
  region = "tor1"
}
