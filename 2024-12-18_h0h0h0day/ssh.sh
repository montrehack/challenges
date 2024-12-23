#!/bin/bash

# Check if a target parameter is provided
if [ $# -eq 0 ]; then
    echo "Error: No target specified: ctfd or challenge"
    echo "Usage: $0 <target>"
    exit 1
fi

TARGET=$1

# Execute the SSH command with the provided target
ssh -i .secrets/ssh root@$(terraform -chdir=terraform/ output -raw ${TARGET}_ip)
