FROM node:dubnium-alpine AS build

COPY --chown=node:node . /app
WORKDIR /app

RUN npm install
RUN npm run build

FROM node:dubnium

RUN apt-get update && \
    apt-get install redis-server zip -y

COPY --from=build --chown=root:root /app/build /app
COPY ./entrypoint.sh /
WORKDIR /app

RUN zip -r /app/static/source.zip /app -x node_modules
RUN chown node:node /app/userdata
RUN mkdir /app/userdata/admin
RUN echo "FLAG{YOURE_GETTING_COAL_THIS_CHRISTMAS}" > /app/userdata/admin/flag

ENV SECRET=Wn7D4NYgt0A72VK6Jwjj8jOFwmWVz3D73Bjwrz88SHe1IuyxtjxtdxAhy8zU
ENV NODE_ENV=production

RUN npm install
USER node

ENTRYPOINT [ "/entrypoint.sh" ]