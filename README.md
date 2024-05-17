### musik

Play YouTube audio playlist in terminal.

Install `ffmpeg` and `mpg123` on your system:

```
sudo apt install -y ffmpeg mpg123
```

Installation:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Usage:

```
python musik.py [YouTube Playlist URL]
```