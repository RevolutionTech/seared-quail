# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    def set_initial_orders(apps, schema_editor):
        MenuItem = apps.get_model("menu", "MenuItem")
        for menuitem in MenuItem.objects.all():
            menuitem.order = menuitem.id
            menuitem.save()

    dependencies = [("menu", "0004_auto_20160829_0617")]

    operations = [migrations.RunPython(set_initial_orders, lambda *args: None)]
