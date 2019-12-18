FROM alpine:latest


RUN	apk add --no-cache nginx php7-bz2 php7-fpm php7-session tini
ENTRYPOINT ["/sbin/tini", "--"]

COPY	nginx.conf /etc/nginx/conf.d/default.conf


# 1,2 (html, index)
COPY	htdocs/ /var/www/localhost/htdocs/

# 3 /etc/passwd
RUN	adduser -g 'FLAG-oehahMaeNahb4Oojushohf1uneegoosh' -D EeWu3f3e

# 4 user's home directories
RUN	chmod 0555 /home/EeWu3f3e
RUN	printf '#FLAG-ceev3sheiYieboonae9ouYai1rooL2tu\n' >>/home/EeWu3f3e/.profile

# 5 /proc listing
COPY	proc-flag.sh /usr/local/bin/daemond
RUN	chmod 0555 /usr/local/bin/daemond

# 6 rce
RUN	mkdir /var/php
RUN	chown nobody /var/php
RUN	chmod u=wx,go= /var/php
RUN	printf 'FLAG-eesiej8ahh2kesh6pheeChoPion4iese\n' >/bu0cie9Aih4phahDuuJah2ohrei9ahci
RUN	chmod 0444 /bu0cie9Aih4phahDuuJah2ohrei9ahci


COPY	init.sh /usr/local/bin/init
RUN	chmod 0555 /usr/local/bin/init

CMD ["/usr/local/bin/init"]
