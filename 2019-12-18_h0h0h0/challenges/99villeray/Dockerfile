FROM tutum/apache-php

RUN apt-get update -y

ADD ./app /var/www/html/

RUN chown www-data:www-data -R /var/www/html
RUN chmod 555 /var/www/html -R

RUN echo 'FLAG{C99VILLERAYGANGGANG}' >> /home/flag.txt

