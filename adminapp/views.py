from django.shortcuts import redirect, render
import io
import csv

from adminapp.models import City, Country, Neighbourhood, Region

# Create your views here.

def import_address_data(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                country_name_csv = row[0].strip().title()
                city_name_csv = row[1].strip().title()
                region_name_csv = row[2].strip().title()
                neighbourhood_name_csv = row[3].strip().title()
                neighbourhood_zip_csv = row[4].strip()
                
                try:
                    Country.objects.get(country_name=country_name_csv)
                except Country.DoesNotExist:
                    country = Country(country_name=country_name_csv)
                    country.save()
                try:
                    City.objects.get(city_name=city_name_csv)
                except City.DoesNotExist:
                    city = City(country=country, city_name=city_name_csv)
                    city.save()

                try:
                    Region.objects.get(region_name=region_name_csv)
                except Region.DoesNotExist:
                    region = Region(city=city ,region_name=region_name_csv)
                    region.save()

                try:
                    Neighbourhood.objects.get(neighbourhood_name=neighbourhood_name_csv)
                except Neighbourhood.DoesNotExist:
                    neighbourhood = Neighbourhood(region=region ,neighbourhood_name=neighbourhood_name_csv, neighbourhood_zip=neighbourhood_zip_csv) 
                    neighbourhood.save()
    return redirect('index')
    
def index(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                country_name_csv = row[0].strip()
                print(country_name_csv)
                country = Country(country_name=country_name_csv)
                country.save()
    return render(request, 'adminapp/index.html')

