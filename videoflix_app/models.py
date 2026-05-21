from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
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
    



               
