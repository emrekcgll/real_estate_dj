from urllib import response
from django.shortcuts import render, redirect
from adminapp.models import City, County, Neighbourhood, Region
import io
import csv
from django.contrib import messages

from modelapp.forms import EstateStatusForm, EstateTypeForm, FromWhoForm, RoomCountForm


def import_operations(request):
    return render(request, "modelapp/importoperations.html")


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


def create_model(request):
    estateTypeForm = EstateTypeForm()
    estateStatusForm = EstateStatusForm()
    fromWhoForm = FromWhoForm()
    roomCountForm = RoomCountForm()
    response = {"estateTypeForm": estateTypeForm,
                "estateStatusForm": estateStatusForm,
                "fromWhoForm": fromWhoForm,
                "roomCountForm": roomCountForm}
    return render(request, "modelapp/create_model.html", response)


def create_estate_type(request):
    if request.method == "POST":
        form = EstateTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
            return redirect("index")
        else:
            messages.error(request, "Something went wrong.")
            return redirect("create_model")


def create_estate_status(request):
    if request.method == "POST":
        form = EstateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
            return redirect("index")
        else:
            messages.error(request, "Something went wrong.")
            return redirect("create_model")


def create_from_who(request):
    if request.method == "POST":
        form = FromWhoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
            return redirect("index")
        else:
            messages.error(request, "Something went wrong.")
            return redirect("create_model")


def create_room_count(request):
    if request.method == "POST":
        form = RoomCountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
            return redirect("index")
        else:
            messages.error(request, "Something went wrong.")
            return redirect("create_model")
