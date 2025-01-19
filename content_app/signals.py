from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from content_app.tasks import convert_480p

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New video created')
        convert_480p(instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            file_480p = f"{instance.video_file.path[:-4]}_480p.mp4"
            os.remove(instance.video_file.path)
            os.remove(file_480p)

