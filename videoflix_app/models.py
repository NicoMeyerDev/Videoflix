from django.db import models

class Video(models.Model):
    """
    Represents a video entry in the platform.
    Stores metadata such as title, description, category and thumbnail.
    The original video file is used as source for HLS conversion.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci-fi', 'Sci-Fi'),
        ('documentary', 'Documentary'),
        ('romance', 'Romance'),

    ])

    def __str__(self):
        return self.title

class VideoFile(models.Model):
    """
    Represents a converted HLS version of a Video.
    Each VideoFile stores the path to the HLS segments for a specific resolution.
    One Video can have multiple VideoFile entries (480p, 720p, 1080p).
    """
    video = models.ForeignKey(Video, related_name='files', on_delete=models.CASCADE)
    hls_path = models.CharField(max_length=255,blank=True, null=True)
    resolution = models.CharField(max_length=20,choices=[
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4K', '4K'),
    ])  
    def __str__(self):
        return f"{self.video.title} - {self.resolution}"    
    



               
