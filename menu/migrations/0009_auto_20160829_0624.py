from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("menu", "0008_auto_20160829_0622")]

    operations = [
        migrations.RenameField(
            model_name="menuitem", old_name="enabled", new_name="show_in_menu"
        ),
        migrations.AddField(
            model_name="menuitem",
            name="user_can_order",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="description",
            field=models.TextField(
                help_text=b"Enter valid HTML", null=True, blank=True
            ),
        ),
    ]
