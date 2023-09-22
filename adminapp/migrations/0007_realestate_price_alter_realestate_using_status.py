# Generated by Django 4.2.2 on 2023-09-21 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_image_remove_address_neighbourhood_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='realestate',
            name='using_status',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]