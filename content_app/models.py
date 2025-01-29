from django.db import models

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    titel_picture_file = models.FileField(upload_to='img', blank=True, null=True)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    

    def __str__(self):
        return self.title