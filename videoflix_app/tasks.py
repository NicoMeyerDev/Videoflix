import os
import subprocess
from videoflix_app.models import Video, VideoFile 

def convert_480p(source, video_id):
    """
    Converts a video file to 480p HLS format.
    Creates the output directory, runs ffmpeg to generate HLS segments,
    and saves the VideoFile entry in the database.
    """
    file_name = os.path.splitext(source)[0]
    output_path = f"{file_name}/480p"
    os.makedirs(output_path, exist_ok=True)
    cmd = 'ffmpeg -i "{}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}/index.m3u8"'.format(source, output_path)
    subprocess.run(cmd, capture_output=True, shell=True)
    # Thumbnail generieren
    thumbnail_path = f"{file_name}_thumbnail.jpg"
    subprocess.run(f'ffmpeg -i "{source}" -ss 00:00:01 -vframes 1 -update 1 "{thumbnail_path}"', shell=True)

    # Thumbnail im Video Model speichern
    video = Video.objects.get(id=video_id)
    video.thumbnail.save(os.path.basename(thumbnail_path), open(thumbnail_path, 'rb'))

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
    subprocess.run(cmd, capture_output=True, shell=True)

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
    subprocess.run(cmd, capture_output=True, shell=True)

    VideoFile.objects.create(
        video=Video.objects.get(id=video_id),
        hls_path=output_path,
        resolution='1080p'
    )