from django.db import models

class ProfileViewer(models.Model):
    user = models.IntegerField()
    viewer_id = models.IntegerField(null=True, blank=True)
    viewername = models.CharField(max_length=100)
    picture_file = models.FileField(upload_to='picture', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self