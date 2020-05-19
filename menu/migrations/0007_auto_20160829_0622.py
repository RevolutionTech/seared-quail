from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("menu", "0006_category_parent")]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ("order",), "verbose_name_plural": "Categories"},
        ),
        migrations.AddField(
            model_name="category",
            name="order",
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]
