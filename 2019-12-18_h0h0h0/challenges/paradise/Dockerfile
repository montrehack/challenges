FROM ubuntu:latest

# Need to install python 2 for pwntools to work properly...
RUN apt-get update && apt-get -y install openssh-server python3 python
RUN useradd flag
RUN mkdir /run/sshd

COPY flag /home/flag
COPY update.py /root/update.py
COPY libprotect.so /root/libprotect.so
COPY sshd_config /etc/ssh/sshd_config
COPY sshd-banner /etc/ssh/sshd-banner

RUN chown -R root:flag /home/flag && chmod 0640 /home/flag/flag.txt

CMD /usr/sbin/sshd && python3 /root/update.py