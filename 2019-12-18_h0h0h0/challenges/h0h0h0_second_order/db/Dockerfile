FROM mariadb:latest

ARG DB_NAME
ARG MYSQL_DATABASE
ARG DB_USER1
ARG DB_USER1_PASS
ARG DB_USER2
ARG DB_USER2_PASS

COPY init_db.sql /tmp/
RUN apt-get update && apt-get -y install gettext-base \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
RUN envsubst < /tmp/init_db.sql >/docker-entrypoint-initdb.d/init_db.sql
