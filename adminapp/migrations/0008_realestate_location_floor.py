# Generated by Django 4.2.2 on 2023-09-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0007_realestate_price_alter_realestate_using_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='location_floor',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
