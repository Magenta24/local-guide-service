# Generated by Django 4.1.7 on 2023-05-06 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("local_guide", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attraction",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="local_guide.discount",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="attraction_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="local_guide.attraction",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="tour_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="local_guide.tour",
            ),
        ),
    ]
