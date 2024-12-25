# Event year
variable "H0H0_YEAR" {
  type = string
}

# Cloudflare info
data "cloudflare_zone" "montrehack" {
  name = "montrehack.ca" # Your domain name
}
