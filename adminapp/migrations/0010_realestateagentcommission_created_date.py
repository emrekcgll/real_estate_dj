# Generated by Django 4.2.5 on 2023-10-08 10:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_realestateagentcommission'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestateagentcommission',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]