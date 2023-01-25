<div><img
                alt="GitHub Actions build status (Lint)"
                src="https://img.shields.io/badge/Maintained%3F-yes-green.svg"> <img
                alt="GitHub Actions build status (Lint)"
                src="https://img.shields.io/github/issues/Mamounx/youtube-downloader.svg"> <img
                alt="GitHub Actions build status (Lint)"
                src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" style="border-radius: 5px"></div>

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
docker build . -t youtube-downloader && docker run -v donwloads:/app/downloads youtube-downloader
```

## Features

- Choose different resolutions to download - default 1080p
