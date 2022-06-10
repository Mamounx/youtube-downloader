FROM python:3.8-slim-buster

WORKDIR /app

ARG VIDEO=""
ARG PLAYLIST=""
ARG RESOLUTION=""

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "main.py", "--v", $VIDEO, "--p", $PLAYLIST, "--r", $RESOLUTION]
RUN python3 main.py --v ${VIDEO}