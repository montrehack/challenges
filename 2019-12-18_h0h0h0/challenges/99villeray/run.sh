#/bin/bash
docker build -t 99villeray . && docker run -d --name 99villeray --expose 80 --net nginx-proxy -e VIRTUAL_HOST=99villeray.pwnctf.io 99villeray
