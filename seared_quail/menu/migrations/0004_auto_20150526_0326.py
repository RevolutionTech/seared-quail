# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def set_initial_orders(apps, schema_editor):
        MenuItem = apps.get_model("menu", "MenuItem")
        for menuitem in MenuItem.objects.all():
            menuitem.order = menuitem.id
            menuitem.save()

    dependencies = [
        ('menu', '0003_auto_20150514_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='menuitem',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_initial_orders, lambda *args: None),
    ]
