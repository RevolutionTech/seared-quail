from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0002_auto_20150506_0116")]

    operations = [
        migrations.AddField(
            model_name="order",
            name="completed",
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        )
    ]
