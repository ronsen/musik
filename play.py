import os

cache_dir = os.path.expanduser('~/.cache')
app_directory = os.path.join(cache_dir, 'musik')

print(app_directory)