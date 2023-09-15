from django.http import JsonResponse
from django.shortcuts import redirect, render
import io
import csv
from adminapp.forms import RealEstateForm

from adminapp.models import City, County, Neighbourhood, RealEstate, Region

# Create your views here.


def index(request):
    return render(request, 'adminapp/index.html')


def import_operations(request):
    return render(request, "adminapp/importoperations.html")


def estates(request):
    return render(request, "adminapp/estates.html")

def estate_create(request):
    form = RealEstateForm()

    response = {"form": form}
    return render(request, "adminapp/estatecreate.html", response)

def estate_list_ajax(request):
    estates = RealEstate.objects.all()
    data = []
    for estate in estates:
        data.append({
            "title": estate.title,
        })
    response = {"data": data}
    return JsonResponse(response)


def import_address_data(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                city_name_csv = row[0].strip().title()
                county_name_csv = row[1].strip().title()
                region_name_csv = row[2].strip().title()
                neighbourhood_name_csv = row[3].strip().title()
                neighbourhood_zip_csv = row[4].strip()
                try:
                    City.objects.get(city_name=city_name_csv)
                except City.DoesNotExist:
                    city = City(city_name=city_name_csv)
                    city.save()
                try:
                    County.objects.get(county_name=county_name_csv)
                except County.DoesNotExist:
                    county = County(city=city, county_name=county_name_csv)
                    county.save()
                try:
                    Region.objects.get(region_name=region_name_csv)
                except Region.DoesNotExist:
                    region = Region(county=county, region_name=region_name_csv)
                    region.save()
                try:
                    Neighbourhood.objects.get(
                        neighbourhood_name=neighbourhood_name_csv)
                except Neighbourhood.DoesNotExist:
                    neighbourhood = Neighbourhood(
                        region=region, neighbourhood_name=neighbourhood_name_csv, neighbourhood_zip=neighbourhood_zip_csv)
                    neighbourhood.save()
    return redirect('import_operations')
