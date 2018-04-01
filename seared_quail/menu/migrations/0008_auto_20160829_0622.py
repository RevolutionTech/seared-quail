# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    def set_initial_orders(apps, schema_editor):
        Category = apps.get_model("menu", "Category")
        for category in Category.objects.all():
            category.order = category.id
            category.save()

    dependencies = [
        ('menu', '0007_auto_20160829_0622'),
    ]

    operations = [
        migrations.RunPython(set_initial_orders, lambda *args: None),
    ]
