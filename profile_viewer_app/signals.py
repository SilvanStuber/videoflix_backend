from .models import ProfileViewer
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

@receiver(post_delete, sender=ProfileViewer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture_file:
        if os.path.isfile(instance.picture_file.path):
            os.remove(instance.picture_file.path)

