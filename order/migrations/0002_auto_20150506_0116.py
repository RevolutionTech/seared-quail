from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="ordermenuitem",
            name="quantity",
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="ordermenuitem",
            name="note",
            field=models.TextField(null=True, blank=True),
        ),
    ]
