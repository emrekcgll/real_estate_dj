# Generated by Django 4.2.5 on 2023-10-11 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_alter_estatestatus_estate_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estatestatus',
            name='estate_status',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='estatetype',
            name='estate_type',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='fromwho',
            name='from_who',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='estate_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estatestatus'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='estate_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estatetype'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='from_who',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.fromwho'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='room_count',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.roomcount'),
        ),
        migrations.AlterField(
            model_name='roomcount',
            name='room_count',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]