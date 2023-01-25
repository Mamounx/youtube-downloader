FROM python:3.8

WORKDIR /app

ARG VIDEO
ARG PLAYLIST
ARG RESOLUTION="1080p"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

# CMD [ "python3", "main.py"]
RUN python3 main.py --v ${VIDEO}