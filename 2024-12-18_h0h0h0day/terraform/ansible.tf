# Generate Ansible inventory file
resource "local_file" "ansible_inventory" {
  content = templatefile("ansible-inventory.tmpl",
    {
      ctfd_ip = digitalocean_droplet.ctfd.ipv4_address
      challenge_ip = digitalocean_droplet.challenge.ipv4_address
      infra_sshprivkey = local_sensitive_file.private_key.filename
    }
  )
  filename = "../ansible/inventory.yml"
  file_permission = "0660"
}
