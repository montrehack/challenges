#!/bin/bash

{ while :; do redis-server; done; } &
{ while :; do node /app/ftp.js; done } &
node /app/http.js