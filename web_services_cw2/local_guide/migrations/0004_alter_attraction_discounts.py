# Generated by Django 4.1.7 on 2023-05-06 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("local_guide", "0003_remove_attraction_discount_attraction_discounts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attraction",
            name="discounts",
            field=models.ManyToManyField(to="local_guide.discount"),
        ),
    ]