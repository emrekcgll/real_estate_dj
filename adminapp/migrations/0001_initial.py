# Generated by Django 4.2.5 on 2023-10-11 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_start_date', models.DateTimeField(auto_now_add=True)),
                ('contract_duration', models.PositiveIntegerField()),
                ('year_rental_price', models.PositiveIntegerField()),
                ('mounth_rental_price', models.PositiveIntegerField()),
                ('rent_payment_method', models.CharField(max_length=200)),
                ('how_to_use_the_rented_property', models.CharField(max_length=200)),
                ('status_of_the_rented_property', models.CharField(max_length=200)),
                ('fixtures_delivered_with_the_rental', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_name', models.CharField(max_length=30)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.city')),
            ],
        ),
        migrations.CreateModel(
            name='EstateBuyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_surname', models.CharField(max_length=200)),
                ('identity_number', models.CharField(blank=True, max_length=11, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstateOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_surname', models.CharField(max_length=200)),
                ('identity_number', models.CharField(blank=True, max_length=11, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstateRenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_surname', models.CharField(max_length=200)),
                ('identity_number', models.CharField(blank=True, max_length=11, null=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstateStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estate_status', models.CharField(choices=[('Kiralık', 'Kiralık'), ('Satılık', 'Satılık')], max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estate_type', models.CharField(choices=[('Daire', 'Daire'), ('Villa', 'Villa'), ('Residence', 'Residence'), ('Müstakil Ev', 'Müstakil Ev')], max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FromWho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_who', models.CharField(choices=[('Emlakçıdan', 'Emlakçıdan'), ('Sahibinden', 'Sahibinden')], max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment_number', models.CharField(max_length=10)),
                ('exterior_door_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('slug', models.SlugField(max_length=300)),
                ('description', models.CharField(max_length=1000)),
                ('estate_number', models.CharField(max_length=10)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('m2_brut', models.CharField(max_length=10)),
                ('m2_net', models.CharField(max_length=10)),
                ('heating', models.CharField(max_length=100)),
                ('using_status', models.CharField(blank=True, max_length=10, null=True)),
                ('building_years', models.CharField(max_length=10)),
                ('building_floor', models.CharField(max_length=10)),
                ('location_floor', models.CharField(max_length=10)),
                ('bathrooms_count', models.CharField(max_length=10)),
                ('within_site', models.BooleanField(default=False)),
                ('site_name', models.CharField(blank=True, max_length=75, null=True)),
                ('is_with_firniture', models.BooleanField(default=False)),
                ('dues', models.CharField(max_length=10)),
                ('is_available_for_loan', models.BooleanField(default=False)),
                ('is_balcony', models.BooleanField(default=False)),
                ('deed_status', models.CharField(max_length=100)),
                ('change', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.city')),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.county')),
                ('estate_buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estatebuyer')),
                ('estate_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estateowner')),
                ('estate_rent_contrat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.contrat')),
                ('estate_renter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estaterenter')),
                ('estate_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estatestatus')),
                ('estate_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.estatetype')),
                ('from_who', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.fromwho')),
            ],
        ),
        migrations.CreateModel(
            name='RoomCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_count', models.CharField(choices=[('1+0', '1+0'), ('1+1', '1+1'), ('2+1', '2+1'), ('3+1', '3+1'), ('4+1', '4+1'), ('4+2', '4+2'), ('5+1', '5+1'), ('5+2', '5+2'), ('5+3', '5+3')], max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(max_length=30)),
                ('county', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.county')),
            ],
        ),
        migrations.CreateModel(
            name='RealEstateAgentCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comission', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('estate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.realestate')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='realestate',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.region'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='room_count',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminapp.roomcount'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='estate_images/')),
                ('real_estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.realestate')),
            ],
        ),
    ]
