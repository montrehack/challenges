# Event year
variable "H0H0_YEAR" {
  type = string
}

# Cloudflare info
data "cloudflare_zone" "montrehack" {
  name = "montrehack.ca" # Your domain name
}

# Droplet size
# good values for larger include c-16-intel
variable "size" {
  type        = string
  description = "Size of the DigitalOcean droplets"
  default     = "s-2vcpu-4gb"  # defaults to small
}
