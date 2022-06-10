# Youtube Downloader

This app will download any given youtube video or youtube playlist

## Requirements

If you run the code localy you need to make virtual environment and run,

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
python main.py --v {} --p {} --r {}
```

or

```bash
docker build . -t youtube-downloader && docker run youtube-downloader
```

## Features

- Choose different resolutions to download - default 1080p
