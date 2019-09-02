from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("menu", "0005_auto_20160829_0618")]

    operations = [
        migrations.AddField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True, to="menu.Category", null=True, on_delete=models.SET_NULL
            ),
        )
    ]
