FROM php:7.0-apache

COPY ./app /app
COPY vhost.conf /etc/apache2/sites-available/000-default.conf

COPY ./start.sh /start.sh

RUN chmod +x /start.sh && /start.sh
