# Generated by Django 4.2.5 on 2023-10-05 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_estatebuyer_realestate_estate_buyer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat',
            name='estate',
        ),
        migrations.RemoveField(
            model_name='contrat',
            name='estate_owner',
        ),
        migrations.RemoveField(
            model_name='contrat',
            name='estate_renter',
        ),
        migrations.AddField(
            model_name='realestate',
            name='estate_rent_contrat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.contrat'),
        ),
    ]