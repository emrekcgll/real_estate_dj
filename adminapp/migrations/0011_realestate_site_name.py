# Generated by Django 4.2.2 on 2023-09-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0010_realestate_heating'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='site_name',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]