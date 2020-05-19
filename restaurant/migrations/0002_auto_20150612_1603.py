from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("restaurant", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="table", name="number", field=models.CharField(max_length=60)
        )
    ]
