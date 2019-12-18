apt-get update
apt-get install --assume-yes strace iputils-ping sudo

chmod 500 -R /app
chmod 700 -R /app/output
chmod 100 /app/strace
chown -R www-data:www-data /app

echo 'ServerName ping-it.owoups.org' >> /etc/apache2/apache2.conf
echo 'www-data ALL = (root) NOPASSWD: /app/strace' > /etc/sudoers

a2enmod rewrite
service apache2 restart
