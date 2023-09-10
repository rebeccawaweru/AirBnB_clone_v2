#!/usr/bin/env bash
# setting up web servers for deployment
sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -fs /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
    	alias /data/web_static/current;
	index index.html index.htm;
    }

    location /redirect_me {
    	return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
    	root /var/www/html;
	internal;
    }
}" > /etc/nginx/sites-available/default

sudo service nginx restart
