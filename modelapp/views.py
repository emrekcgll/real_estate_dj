from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import City, County, EstateStatus, EstateType, FromWho, Neighbourhood, Region, RoomCount
from modelapp.forms import EstateStatusForm, EstateTypeForm, FromWhoForm, RoomCountForm
import io
import csv


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


def create_estate_type(request):
    if request.method == "POST":
        form = EstateTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateTypeForm()
    return render(request, "modelapp/create_estate_type.html", {"form": form})


def create_estate_status(request):
    if request.method == "POST":
        form = EstateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateStatusForm()
    return render(request, "modelapp/create_estate_status.html", {"form": form})


def create_from_who(request):
    if request.method == "POST":
        form = FromWhoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = FromWhoForm()
    return render(request, "modelapp/create_from_who.html", {"form": form})


def create_room_count(request):
    if request.method == "POST":
        form = RoomCountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = RoomCountForm()
    return render(request, "modelapp/create_room_count.html", {"form": form})


def show_estate_type(request):
    estate_types = EstateType.objects.all()
    data = []
    for i in estate_types:
        data.append({
            "estate_type": i.estate_type,
        })
    response = {"data": data}
    return JsonResponse(response)


def show_estate_status(request):
    estate_status = EstateStatus.objects.all()
    data = []
    for i in estate_status:
        data.append({
            "estate_status": i.estate_status,
        })
    response = {"data": data}
    return JsonResponse(response)


def show_from_who(request):
    from_whos = FromWho.objects.all()
    data = []
    for i in from_whos:
        data.append({
            "from_who": i.from_who,
        })
    response = {"data": data}
    return JsonResponse(response)


def show_room_count(request):
    room_counts = RoomCount.objects.all()
    data = []
    for i in room_counts:
        data.append({
            "room_count": i.room_count,
        })
    response = {"data": data}
    return JsonResponse(response)


def delete_estate_type(request, pk):
    pass


def delete_estate_status(request, pk):
    pass


def delete_from_who(request, pk):
    pass


def delete_room_count(request, pk):
    pass
