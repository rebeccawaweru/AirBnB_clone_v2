#!/usr/bin/env bash
# setting up web servers for deployment
sudo apt-get -y update
sudo apt-get -y install nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
touch /data/web_static/releases/test/index.html
ln -fs /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
echo "<html>\n\t<head>\n\t</head>\n\t\t<body>\n\t\t\tHoberlton School\n\t\t</body>\n</html>" > /data/web_static/releases/test/index.html
sed -i "s/# Only/\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/; \n\t\tautoindex off;\n\t}\n \n\t# Only/" /etc/nginx/sites-available/default
sudo service nginx restart
