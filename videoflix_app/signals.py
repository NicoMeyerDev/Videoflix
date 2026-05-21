import shutil

from videoflix_app.tasks import convert_480p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
import shutil


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Converts uploaded video to 480p and creates HLS files.
    """

    if created:
        convert_480p(instance.video_file.path)

@receiver(post_delete, sender=Video)

def video_post_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Video` object is deleted.
    """

    if instance.video_file:
    # Konvertierte Ordner löschen
        for video_file in instance.files.all():
            if os.path.exists(video_file.hls_path):
                shutil.rmtree(video_file.hls_path)
    
    # Originaldatei löschen
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)


