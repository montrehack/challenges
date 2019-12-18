FROM gradle


RUN apt update && apt-get -y install openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

RUN useradd spring -m
# TODO: Change root passwd

COPY flag.txt /

RUN mkdir -p /home/spring/server/src 
RUN mkdir /home/spring/server/.gradle && chown spring:spring /home/spring/server/.gradle
RUN mkdir /home/spring/server/build && chown spring:spring /home/spring/server/build
COPY build.gradle /home/spring/server
COPY settings.gradle /home/spring/server
COPY src /home/spring/server/src

WORKDIR /home/spring/server

USER spring
RUN gradle build
CMD gradle bootRun
