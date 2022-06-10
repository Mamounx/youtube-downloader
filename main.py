from pytube import YouTube, Stream, Playlist
import argparse
import sys
import logging
import pathlib
from interface.args import Args

class YoutubeDownloader():
    def __init__(self, args) -> None:
        self.args: Args = args
        self.download_path = f'{pathlib.Path().resolve()}/downloads'
        self.video = None
        self.playlist = None
        self.resolution = None
        self.fetch_args()
        self.start()

    def fetch_args(self):
        self.video = self.args.video
        self.playlist = self.args.playlist
        self.resolution = self.args.resolution

    def start(self):
        yt = YouTube(self.video, on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
        # download_playlist = Playlist()
        stream_1080: Stream = yt.streams.filter(res="1080p")[0]
        if not stream_1080:
            return self.on_error('1080p video not found!')
        print(stream_1080.exists_at_path(self.download_path))
        stream_1080.download(self.download_path )

    def on_progress(self, stream: Stream, chunk, remaining_bytes):
        downloaded = stream._filesize - remaining_bytes
        done = int(50 * downloaded /  stream._filesize)
        sys.stdout.write("\r[{}{}]".format("=" * done, " " * (50 - done)))
        sys.stdout.flush()
    
    def on_complete(self, stream: Stream, chunk):
        print(f'{stream.title} has been successfully downloaded in \n {stream.get_file_path()}')

    def on_error(self, error):
        logging.error(error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Youtube Downloader")
    parser.add_argument(
        "--p",
        dest="playlist",
        help="Download Playlist",
        default="",
        type=str,
    )
    parser.add_argument(
        "--v",
        dest="video",
        help="Download Video",
        default="",
        type=str,
    )
    parser.add_argument(
        "--r",
        dest="resolution",
        help="Download Resolution",
        default="1080p",
        type=str,
    )

    args: Args = parser.parse_args()    
    yd = YoutubeDownloader(args)
