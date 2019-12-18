FROM php:7.4-apache

COPY ./app /app
COPY vhost.conf /etc/apache2/sites-available/000-default.conf

COPY logrotate /etc/logrotate.d/ping-it

COPY ./start.sh /start.sh
COPY ./strace /app/strace

RUN chmod +x /start.sh && /start.sh
