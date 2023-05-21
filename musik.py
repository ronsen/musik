import os
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
    audio = yt.streams.filter(only_audio=True).first()
    f = audio.download(output_path='out')
    
    file_name = os.path.basename(f)
    print('Playing: %s' % file_name)

    playsound.playsound(f, True)
    
    os.remove(f)