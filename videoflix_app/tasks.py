import os
import subprocess
from videoflix_app.models import Video, VideoFile 

def convert_480p(source, video_id):
    """
    Konvertiert eine Videodatei in das HLS-Format mit 480p Auflösung.
    Erstellt den Ausgabeordner, führt ffmpeg aus um HLS-Segmente zu erzeugen
    und speichert den VideoFile Eintrag in der Datenbank.
    """
    file_name = os.path.splitext(source)[0]
    output_path = f"{file_name}/480p"
    os.makedirs(output_path, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}/index.m3u8"'.format(source, output_path)
    subprocess.run(cmd, capture_output=True)

    VideoFile.objects.create(
        video=Video.objects.get(id=video_id),
        hls_path=output_path,
        resolution='480p'
    )

def convert_720p(source, video_id):
    file_name = os.path.splitext(source)[0]
    output_path = f"{file_name}/720p"
    os.makedirs(output_path, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}/index.m3u8"'.format(source, output_path)
    subprocess.run(cmd, capture_output=True)

    VideoFile.objects.create(
        video=Video.objects.get(id=video_id),
        hls_path=output_path,
        resolution='720p'
    )

def convert_1080p(source, video_id):    
    file_name = os.path.splitext(source)[0]
    output_path = f"{file_name}/1080p"
    os.makedirs(output_path, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}/index.m3u8"'.format(source, output_path)
    subprocess.run(cmd, capture_output=True)

    VideoFile.objects.create(
        video=Video.objects.get(id=video_id),
        hls_path=output_path,
        resolution='1080p'
    )