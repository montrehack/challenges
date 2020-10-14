FROM ubuntu:18.04
RUN apt-get -y update && apt-get install -y xinetd && \
    useradd -m heap && \
    chmod 700 -R /home/heap

COPY ./rel/chal /home/heap/
COPY ./rel/xinetd.conf /etc/xinetd.d/heap
COPY ./rel/art.txt /art.txt
COPY ./rel/flag.txt /etc/flag.txt

RUN chmod 644 /etc/flag.txt


CMD ["/usr/sbin/xinetd", "-dontfork"]
