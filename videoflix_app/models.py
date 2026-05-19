from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        # Add more categories as needed
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
        return f"{self.video.title} - {self.format} - {self.resolution}"    
    



               
