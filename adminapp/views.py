from django.shortcuts import redirect, render
import io
import csv

from adminapp.models import City, Country, Neighbourhood, Region

# Create your views here.

def import_country(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                country_name_csv = row[0].strip()
                country = Country(country_name=country_name_csv)
                country.save()
    return redirect('index')
    
def import_city(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                city_name_csv = row[1].strip().title()
                country_id = row[2].strip()
                country = City(country_id=country_id, city_name=city_name_csv)
                country.save()
    return redirect('index')

def import_region(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                region_name_csv = row[2].strip().title()
                city_id_csv = row[1].strip()
                region = Region(city_id=city_id_csv, region_name=region_name_csv)
                region.save()
    return redirect('index')

def import_neighbourhood(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                neighbourhood_name_csv = row[2].strip()
                neighbourhood_zip = row[3].strip()
                region_id_csv = row[1].strip()
                neighbourhood = Neighbourhood(region_id=region_id_csv, neighbourhood_name=neighbourhood_name_csv, neighbourhood_zip=neighbourhood_zip)
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

