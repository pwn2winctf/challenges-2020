from debian:10

#just infra stuff
RUN useradd -M butcher 
RUN useradd manager 

RUN apt update && apt install -y python3 && apt-get install -y procps && apt install -y python3-pip --fix-missing && pip3 install psutil

WORKDIR /home/manager

COPY ./src/su /etc/pam.d/su
COPY ./src/init.sh ./init.sh
COPY ./src/daemon.py daemon.py
COPY ./src/clean ./clean

RUN chown manager /home/manager
RUN chmod 700 -R /home/manager
RUN chown manager ./daemon.py
RUN chmod 4711  ./clean

ENV HOST="0.0.0.0"
ENV PORT="1337"
ENV NUSERS="800"
ENV TIME_TO_SLEEP="5"
ENV TIMEOUT="10"
ENV INTERVAL_PER_IP="25"
ENV MINIMUM_FREQ="1000"

#allow healthcheck ip to connect to the machine without waiting
ENV ALLOWED_IP="10.138.0.6"
ENV BLOCKED_IP=""
ENV MAX_FILE_SIZE="30000"

CMD  ./init.sh

#chall stuff
COPY ./src/libemojinet.so /lib/x86_64-linux-gnu/libemojinet.so
COPY ./src/encoder ./encoder
RUN chmod 700 encoder



