# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-16 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0018_auto_20201109_1024'),
        ('repository', '0020_vq_title_abstracts'),
    ]

    operations = [
        migrations.AddField(
            model_name='preprintauthor',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preprintauthor',
            name='affiliation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterModelOptions(
            name='author',
            options={},
        ),
        migrations.AlterField(
            model_name='preprintauthor',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='repository.Author'),
        ),
    ]
