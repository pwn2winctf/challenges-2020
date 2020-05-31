FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
#installing gosu , node and npm

RUN set -eux; \
	apt-get update; \
	apt-get install -y gosu; \
	apt-get install -y vim; \
	apt install -y nodejs;\
	apt install -y npm;\
	apt-get install -y gconf-service libasound2 libatk1.0-0 chromium-browser libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget; \
	rm -rf /var/lib/apt/lists/*; \
# verify that the binary works
	gosu nobody true


WORKDIR /usr/src/app


COPY . .

RUN npm install . --save

RUN groupadd -r gnx && useradd --no-log-init -G audio,video -m -r -g gnx gnx

RUN chown -R root:root /usr/src/app; \
	 chmod 770 /usr/src/app/; \
	 mv /usr/src/app/script /home/gnx/; \
	 chown -R root:gnx /home/gnx/script; \
	 chmod  -R 2755 /home/gnx/script; \
	 chmod 777 /home/gnx/script/xxe_secret;

RUN cd /home/gnx/script;npm install --save; npm install -g puppeteer@2.1.0 --unsafe-perm --save

EXPOSE 31337

CMD ["node" , "/usr/src/app/index.js"]
