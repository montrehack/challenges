apt-get update
apt-get install --assume-yes python3 python3-pip curl wget

pip3 install pillow numpy

chmod 500 -R /app
chown -R www-data:www-data /app
