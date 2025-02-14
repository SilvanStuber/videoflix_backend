import subprocess
from pathlib import Path

def convert_720p(source):
    new_file_name = f"{source[:-4]}_720p.mp4"
    cmd = 'ffmpeg -y -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run =   subprocess.run(cmd, check=True)

def convert_480p(source):
    new_file_name = f"{source[:-4]}_480p.mp4"
    cmd = 'ffmpeg -y -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run =   subprocess.run(cmd, check=True)

