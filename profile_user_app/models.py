from django.db import models

class Profile(models.Model):
    user = models.IntegerField()
    username = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self