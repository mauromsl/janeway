# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 13:02
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_pinnedarticle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pinnedarticle',
            options={'ordering': ('sequence',)},
        ),
        migrations.AlterField(
            model_name='issue',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.cover_images_upload_path),
        ),
        migrations.AlterField(
            model_name='issue',
            name='large_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.issue_large_image_path),
        ),
        migrations.AlterField(
            model_name='journal',
            name='default_cover_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.cover_images_upload_path),
        ),
        migrations.AlterField(
            model_name='journal',
            name='default_large_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.cover_images_upload_path),
        ),
        migrations.AlterField(
            model_name='journal',
            name='favicon',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.cover_images_upload_path),
        ),
        migrations.AlterField(
            model_name='journal',
            name='header_image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/ajrbyers/Code/janeway/src/media'), upload_to=journal.models.cover_images_upload_path),
        ),
    ]
