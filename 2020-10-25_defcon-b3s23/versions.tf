terraform {
  required_providers {
    ansible = {
      source = "nbering/ansible"
      version = "1.0.4"
    }
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.1.0"
    }
    null = {
      source = "hashicorp/null"
      version = "~> 2.1.2"
    }
  }
  required_version = ">= 0.13"
}
