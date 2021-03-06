from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("menu", "0003_auto_20150514_2203")]

    operations = [
        migrations.AlterModelOptions(
            name="category", options={"verbose_name_plural": "Categories"}
        ),
        migrations.AlterModelOptions(name="menuitem", options={"ordering": ("order",)}),
        migrations.AddField(
            model_name="menuitem",
            name="order",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]
