# Generated by Django 4.1.4 on 2022-12-16 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_monthstat_calibration_came_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthstat',
            name='calibration_came_from',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='monthstat',
            name='calibration_goes_to',
            field=models.CharField(max_length=1000),
        ),
    ]
