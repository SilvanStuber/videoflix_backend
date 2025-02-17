import subprocess
from pathlib import Path


def convert_720p(source):
    new_file_name = f"{source[:-4]}_720p.mp4"
    cmd = [
        '/usr/bin/ffmpeg', '-y', '-i', source, '-s', 'hd720', 
        '-c:v', 'libx264', '-crf', '28', 
        '-c:a', 'aac', '-strict', '-2', 
        '-threads', '1', 
        new_file_name
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Video erfolgreich konvertiert zu: {new_file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Konvertierung des Videos: {e}")
    except FileNotFoundError:
        print("ffmpeg nicht gefunden. Bitte stelle sicher, dass ffmpeg korrekt installiert ist.")
    except Exception as e:
        print(f"Ein unbekannter Fehler ist aufgetreten: {e}")


def convert_480p(source):
    new_file_name = f"{source[:-4]}_480p.mp4"
    cmd = [
        '/usr/bin/ffmpeg', '-y', '-i', source, '-s', 'hd480', 
        '-c:v', 'libx264', '-crf', '28', 
        '-c:a', 'aac', '-strict', '-2', 
        '-threads', '1',  
        new_file_name
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Video erfolgreich konvertiert zu: {new_file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Konvertierung des Videos: {e}")
    except FileNotFoundError:
        print("ffmpeg nicht gefunden. Bitte stelle sicher, dass ffmpeg korrekt installiert ist.")
    except Exception as e:
        print(f"Ein unbekannter Fehler ist aufgetreten: {e}")
