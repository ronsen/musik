import os
import sys
import subprocess
from pytube import Playlist, YouTube
from urllib.parse import urlparse, parse_qs
import playsound

def main(playlist_url):
    playlist = Playlist(playlist_url)
    directory = album(playlist_url)

    for video_url in playlist.video_urls:
        video = YouTube(video_url)

        try:
            audio = video.streams.filter(only_audio=True).first()       
            file_path = audio.download(output_path=directory)
            audio_path = convert(file_path)
            play(audio_path)
        except Exception as e:
            print('Error processing: %s' % video_url)
        

def album(url):
    parsed_url = urlparse(url)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)
    
    list_id = query_params['list'][0]
    directory = 'outputs/' + list_id

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

def convert(input_file):
    output_file = input_file.replace('.mp4', '.mp3')

    if not os.path.exists(output_file):
        command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'libmp3lame', output_file]
        subprocess.call(command)

    os.remove(input_file)

    return output_file

def play(file_path):
    file_name = os.path.basename(file_path)
    print('Playing: %s' % file_name)

    playsound.playsound(file_path, True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please provide YouTube playlist URL to continue.")
        sys.exit()
    
    main(sys.argv[1])