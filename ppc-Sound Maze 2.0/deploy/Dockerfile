FROM python

COPY *.mp3 /opt/
COPY sound_maze.py /opt/
COPY secrets.py /opt/

RUN pip3 install -U numpy

EXPOSE 31337

WORKDIR /opt
CMD python3 sound_maze.py
