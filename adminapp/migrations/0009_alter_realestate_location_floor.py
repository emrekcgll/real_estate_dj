# Generated by Django 4.2.5 on 2023-10-20 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0008_alter_realestate_building_floor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='location_floor',
            field=models.IntegerField(max_length=2),
        ),
    ]