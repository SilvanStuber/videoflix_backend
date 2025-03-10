# Generated by Django 5.1.4 on 2025-01-27 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_viewer_app', '0003_profileviewer_picture_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileviewer',
            name='picture_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profileviewer',
            name='picture_file',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
