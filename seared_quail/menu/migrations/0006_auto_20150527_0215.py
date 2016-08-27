# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def set_initial_orders(apps, schema_editor):
        Category = apps.get_model("menu", "Category")
        for category in Category.objects.all():
            category.order = category.id
            category.save()

    dependencies = [
        ('menu', '0005_category_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_initial_orders, lambda *args: None),
    ]
