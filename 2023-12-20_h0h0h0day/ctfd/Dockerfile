FROM ctfd/ctfd:3.4.3

# Install git
USER root
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends git

USER 1001
WORKDIR /opt/CTFd/CTFd/plugins/
RUN git clone --depth=1 --branch=main https://github.com/alxbl/ctfd-toastee.git toastee && \
    rm -rf toastee/.git/
RUN git clone --depth=1 https://github.com/sigpwny/ctfd-discord-webhook-plugin.git discord-webhook && \
    rm -rf discord-webhook/.git/
#RUN git clone --depth=1 --branch Pourliver-patch-1 https://github.com/Pourliver/ctfd-discord-webhook-plugin.git discord-webhook && \

USER root
RUN pip install -r toastee/requirements.txt
RUN pip install -r discord-webhook/requirements.txt

USER 1001
WORKDIR /opt/CTFd
