# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuitem_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='img',
            field=models.ImageField(upload_to=b'img/menuitem', null=True, verbose_name=b'Image', blank=True),
        ),
    ]
