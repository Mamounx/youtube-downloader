from pytube import YouTube, Stream, Playlist
import argparse
import sys
import logging
import pathlib
import ffmpeg
import json
from interface.args import Args
from os import listdir
from os.path import isfile, join
class YoutubeDownloader():
    def __init__(self, args) -> None:
        self.args: Args = args
        self.download_path = f'{pathlib.Path().resolve()}/downloads'
        self.temp_audio_path = f'{pathlib.Path().resolve()}/temp_audio'
        self.temp_video_path = f'{pathlib.Path().resolve()}/temp_video'
        self.existing_files  = [f for f in listdir(self.download_path) if isfile(join(self.download_path, f))]
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
        if self.video:
            self.donwload_video()
        else:
            self.download_playlist()

    def donwload_video(self):
        yt = YouTube(self.video, on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
        stream_1080 = yt.streams.filter(resolution=self.resolution, progressive=True)
        print(f"Download path: {self.download_path}")
        print(f"Downloading: ({yt.title})")
        if not stream_1080:
            print("Video in 1080p has no audio, downloading different resolution settings!")
            stream_1080 = yt.streams.filter(progressive=True)

        try:
            stream_1080: Stream = stream_1080[-1]
        except IndexError as e:
            self.on_error(f"No streams found for download! {e}")


        # if not stream_1080:
        #     return self.on_error('1080p video not found!')

        stream_1080.download(self.download_path)

    def download_playlist(self):
        try:
            download_playlist = Playlist(self.playlist)
            for video in download_playlist.videos:            
                print(f"Downloading: ({video.title})")
                video.register_on_progress_callback = self.on_progress
                video.register_on_complete_callback = self.on_complete
                try:
                    stream_1080: Stream = video.streams.filter(resolution=self.resolution)[0]

                    if not stream_1080:
                        print("Video in 1080p has no audio, downloading different resolution settings!")
                        stream_1080: Stream = video.streams.filter(progressive=True)
                    video_stream: Stream = video.streams.filter(resolution=self.resolution)[0]
                    audio_stream: Stream = video.streams.filter(progressive=True)[-1]
                    video_stream.on_progress = self.on_progress
                    stream_1080: Stream = stream_1080[-1]

                    # if not stream_1080:
                    #     return self.on_error(f'{video.title} does not have 1080p resolution!')

                    video_name = video_stream.get_file_path().split('/')[-1]
                    audio_name = audio_stream.get_file_path().split('/')[-1]
                except IndexError as e:
                    self.on_error(f"No streams found for download! {e}")

                if video_name in self.existing_files:
                    print(f'({video.title}) already exist in -> {self.download_path}')
                    continue
                video_stream.download(self.temp_video_path)
                audio_stream.download(self.temp_audio_path)
                            
                video_path = f'{self.temp_video_path}/{video_name}'
                audio_path = f'{self.temp_audio_path}/{audio_name}'

                print(video_path, audio_path)
                input_video = ffmpeg.input(video_path)
                input_audio = ffmpeg.input(audio_path)
                print(f'{self.download_path}/{video_name}')
                print(input_video, input_audio)
                ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{self.download_path}/{video_name}').run()

                # stream_1080.download(self.download_path)

        except Exception as e:
            self.on_error(e)

    def on_progress(self, stream: Stream, chunk, remaining_bytes):
        downloaded = stream._filesize - remaining_bytes
        done = int(50 * downloaded /  stream._filesize)
        sys.stdout.write("\r[{}{}]".format("=" * done, " " * (50 - done)))
        sys.stdout.flush()
    
    def on_complete(self, stream: Stream, chunk):
        print(f'{stream.title} has been successfully downloaded in \n {stream.get_file_path()}')

    def on_error(self, error):
        print(error)
        logging.error(error)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Youtube Downloader")
    parser.add_argument(
        "--p",
        dest="playlist",
        help="Download Playlist",
        default="https://www.youtube.com/watch?v=oxXpB9pSETo&list=PLZzTW0IEkSwO_a3jnzqVa2gm0RWFXer-x&index=1",
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
