# -*- coding: utf-8 -*-
import re
from django.db import migrations

REGEX =  re.compile("{{ journal.site_url }}{% url '(\w+)' ([\w\ \.]*)%}")
REVERSE_REGEX = re.compile("{% journal_url '(\w+)' ([\w\ \.]*)%}")
OUTPUT = "{%% journal_url '%s' %s%%}"
REVERSE_OUTPUT = "{{ journal.site_url }}{%% url '%s' %s%%}"

def replace_matches(out_tepmplate, match):
    view_name = match.group(1)
    args = match.group(2)
    args_string = " ".join(args.split(" "))
    return out_tepmplate % (view_name, args_string)

def replace_bad_urls(apps, schema_editor):
    SettingValueTranslation = apps.get_model('core', 'SettingValueTranslation')
    settings = SettingValueTranslation.objects.all()
    re_func = partial(replace_matches, OUTPUT)
    for setting in settings:
        setting.value = re.sub(REGEX, re_func, setting.value)
        setting.save()

def reverse_code(apps, schema_editor):
    SettingValueTranslation = apps.get_model('core', 'SettingValueTranslation')
    settings = SettingValueTranslation.objects.all()
    re_func = partial(replace_matches, REVERSE_OUTPUT)
    for setting in settings:
        setting.value = re.sub(REVERSE_REGEX, re_func, setting.value)
        setting.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20190201_1015'),
    ]

    operations = [
        migrations.RunPython(replace_bad_urls, reverse_code=migrations.RunPython.noop),
    ]
