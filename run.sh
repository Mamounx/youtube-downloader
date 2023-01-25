USER=m
USER_HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"

source $USER_HOME/.virtualenvs/youtube-downloader/bin/activate
python main.py --v https://www.youtube.com/watch?v=6euC2PqutvM