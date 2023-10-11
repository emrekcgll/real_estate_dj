# Generated by Django 4.2.5 on 2023-10-11 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatetype',
            name='estate_type',
            field=models.CharField(choices=[('DAIRE', 'Daire'), ('VILLA', 'Villa'), ('RESIDENCE', 'Residence'), ('MUSTAKIL_EV', 'Müstakil Ev')], max_length=30, unique=True),
        ),
    ]