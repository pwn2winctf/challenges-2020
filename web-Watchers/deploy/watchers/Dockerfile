FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# install web server
RUN apt update && apt install -y apache2 curl php php-pear php-dev libapache2-mod-php php-curl wget iptables git net-tools iproute2 chromium-browser cron

# install node
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -; \
apt update && apt install -y nodejs

# install npm dependencies
# I used the latest version in my challenge but as soon as i'm publishing it, i'm defining a working one
RUN npm install -g wappalyzer@6.0.2 --unsafe-perm --save

# setup webserver
WORKDIR /var/www/html

COPY . .

WORKDIR /var/www/

RUN chown -R www-data:www-data . && \
mv html/secrets.php . && \
mv html/weaponlyzer.php . && \
chmod 777 -R html/pages && \
echo 'ServerName localhost' >> /etc/apache2/apache2.conf && \
sed -i 's/Options Indexes FollowSymLinks/Options -Indexes/' /etc/apache2/apache2.conf && \
sed -i 's/AllowOverride none/AllowOverride All/i' /etc/apache2/apache2.conf && \
a2enmod rewrite && \
service apache2 restart

# expose server port
EXPOSE 80

# start
CMD /usr/sbin/apache2ctl -D FOREGROUND
