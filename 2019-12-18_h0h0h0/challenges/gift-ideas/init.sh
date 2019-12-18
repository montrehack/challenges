#!/bin/sh
##
set -eu

[ -d /run/nginx ] || mkdir /run/nginx
chown nginx:nginx /run/nginx
/usr/sbin/nginx
/usr/sbin/php-fpm7
exec /usr/local/bin/daemond
