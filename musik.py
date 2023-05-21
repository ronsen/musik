import sys
from pytube import Playlist, YouTube
import playsound

if len(sys.argv) == 1:
    print("Please provide YouTube playlist URL to continue.")
    sys.exit()
    
youtube_url = sys.argv[1]
playlist = Playlist(youtube_url);

for url in playlist.video_urls:
    yt = YouTube(url)
    yt.streams.filter(only_audio=True)
    audio = yt.streams.filter(only_audio=True).first()
    out = audio.download(output_path='out')
    print(out)
    playsound.playsound(out, True)