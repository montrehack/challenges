FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8
RUN apk --update add bash nano curl tar
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
COPY ./app /app

RUN cd /tmp && curl -Ls https://github.com/dustinblackman/phantomized/releases/download/2.1.1/dockerized-phantomjs.tar.gz | tar xz &&\
    cp -R lib lib64 / &&\
    cp -R usr/lib/x86_64-linux-gnu /usr/lib &&\
    cp -R usr/share /usr/share &&\
    cp -R etc/fonts /etc &&\
    curl -k -Ls https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 | tar -jxf - &&\
    cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

RUN pip install -r /var/www/requirements.txt
RUN python /app/createdb.py
