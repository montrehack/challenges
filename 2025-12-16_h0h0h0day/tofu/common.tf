# Upstream NorthSec Cloud Incus
data "incus_project" "montrehack" {
  name = "montrehack"
}

data "incus_profile" "default" {
  name = "default"
  project = data.incus_project.montrehack.name
}

data "incus_network" "default" {
  name = "default"
  project = data.incus_project.montrehack.name
}


# Upstream Cloudflare
data "cloudflare_zone" "montrehack" {
  name = "montrehack.ca" # Your domain name
}
