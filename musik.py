import os
import subprocess
from pytube import Playlist, YouTube
from urllib.parse import urlparse, parse_qs
import argparse


def main(playlist_url, dir):
    playlist = Playlist(playlist_url)
    directory = album(playlist_url, dir)

    files = os.listdir(directory)

    if (len(files) > 0):
        answer = input("Directory is not empty. Play? (Y/n): ")

        if answer.upper() == 'Y':
            play_album(directory)
        else:
            download(playlist, directory)
    else:
        download(playlist, directory)


def album(url, dir):
    cache_dir = os.path.expanduser('~/.cache')
    app_directory = dir if dir else os.path.join(cache_dir, 'musik')

    if not os.path.exists(app_directory):
        os.makedirs(app_directory)

    parsed_url = urlparse(url)
    query_string = parsed_url.query
    query_params = parse_qs(query_string)

    list_id = query_params['list'][0]
    directory = app_directory + '/' + list_id

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def convert(input_file):
    output_file = input_file.replace('.mp4', '.mp3')

    if not os.path.exists(output_file):
        command = ['ffmpeg', '-i', input_file, '-vn',
                   '-acodec', 'libmp3lame', output_file]
        subprocess.call(command)

    os.remove(input_file)

    return output_file


def download(playlist, directory):
    for video_url in playlist.video_urls:
        video = YouTube(video_url)

        try:
            audio = video.streams.filter(only_audio=True).first()
            file_path = audio.download(output_path=directory)

            audio_path = convert(file_path)
            play(audio_path)
        except Exception as e:
            print('Error processing: %s' % video_url)


def play_album(directory):
    for file in os.listdir(directory):
        audio_path = directory + '/' + file
        play(audio_path)


def play(file_path):
    file_name = os.path.basename(file_path)
    print('Playing: %s' % file_name)

    os.system("mpg123 " + file_path)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('url', help='Specify YouTube playlist')
        parser.add_argument('-d', '--directory', help='Specify cache directory')

        args = parser.parse_args()

        main(args.url, args.directory)
    except KeyboardInterrupt:
        print('Bye.')
