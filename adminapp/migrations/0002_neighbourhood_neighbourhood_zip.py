# Generated by Django 4.2.5 on 2023-09-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighbourhood',
            name='neighbourhood_zip',
            field=models.CharField(max_length=10),
            preserve_default=False,
        ),
    ]
