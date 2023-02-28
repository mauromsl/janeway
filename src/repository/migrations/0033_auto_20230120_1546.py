# Generated by Django 3.2.16 on 2023-01-20 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_auto_20230120_1546'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('press', '0027_auto_20220107_1219'),
        ('repository', '0032_repository_submission_notification_recipients'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preprintaccess',
            options={'verbose_name_plural': 'preprint access records'},
        ),
        migrations.RemoveField(
            model_name='preprintauthor',
            name='author',
        ),
        migrations.AlterField(
            model_name='preprintaccess',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.country'),
        ),
        migrations.AlterField(
            model_name='preprintaccess',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.preprintfile'),
        ),
        migrations.AlterField(
            model_name='preprintauthor',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='preprintversion',
            name='moderated_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.versionqueue'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='press',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='press.press'),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.comment'),
        ),
    ]