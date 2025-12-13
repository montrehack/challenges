# Generate Ansible inventory file
resource "local_file" "ansible_inventory" {
  content = templatefile("ansible-inventory.tmpl",
    {
      ctfd_ip = var.CTFD_EXTERNAL_IPV4
      challenge_ip = var.CHALLENGE_EXTERNAL_IPV4
      infra_sshprivkey = local_sensitive_file.private_key.filename
    }
  )
  filename = "../ansible/inventory.yml"
  file_permission = "0660"
}
