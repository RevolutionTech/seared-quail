from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("restaurant", "0001_initial"), ("menu", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "table",
                    models.ForeignKey(to="restaurant.Table", on_delete=models.CASCADE),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="OrderMenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("note", models.TextField()),
                (
                    "menuitem",
                    models.ForeignKey(to="menu.MenuItem", on_delete=models.CASCADE),
                ),
                (
                    "order",
                    models.ForeignKey(to="order.Order", on_delete=models.CASCADE),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
