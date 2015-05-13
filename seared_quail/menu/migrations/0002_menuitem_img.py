# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='img',
            field=models.ImageField(null=True, upload_to=b'img/menuitem/', blank=True),
            preserve_default=True,
        ),
    ]
