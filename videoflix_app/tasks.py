import subprocess

def convert_480p(source):
    new_file_name = source.replace('.mp4', '_480p.mp4')  # TODO - Alter name + _480p.mp4
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.run(cmd, capture_output=True)