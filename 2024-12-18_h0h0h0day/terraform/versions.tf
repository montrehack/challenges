terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      # temporary pin on 4.48 because 4.49 had checksum issues
      version = "~> 4.48.0"
    }
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    null = {
      source = "hashicorp/null"
      version = "~> 2.1.2"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
  required_version = ">= 0.13"
}
