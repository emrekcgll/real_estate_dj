from django.http import JsonResponse
from django.shortcuts import redirect, render
from adminapp.forms import RealEstateForm
from adminapp.models import County, Image, RealEstate, Region


def index(request):
    return render(request, 'adminapp/index.html')


def estates(request):
    return render(request, "adminapp/estates.html")


def estate_create(request):
    if request.method == "POST":
        form = RealEstateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            county = request.POST.get("county")
            region = request.POST.get("region")
            county_instance = County.objects.get(pk=county)
            region_instance = Region.objects.get(pk=region)
            data.county = county_instance
            data.region = region_instance
            data.save()

            estate_instance = RealEstate.objects.get(pk=data.pk)
            files = request.FILES.getlist("image")
            for image in files:
                Image.objects.create(real_estate=estate_instance, image=image)
            return redirect("estates")
    else:
        form = RealEstateForm()
    response = {"form": form}
    return render(request, "adminapp/estatecreate.html", response)


def estate_list_ajax(request):
    estates = RealEstate.objects.all().order_by("-created_date")
    data = []
    for estate in estates:
        image = Image.objects.filter(real_estate=estate.pk).first()
        data.append({
            "image": image.image.url,
            "title": estate.title,
            "city": estate.city.city_name,
            "county": estate.county.county_name,
            "region": estate.region.region_name,
            "room_count": estate.room_count.room_count,
        })
    response = {"data": data}
    return JsonResponse(response)


def get_county_by_city_id(request, city_id):
    city_id = int(city_id)
    county = County.objects.filter(city=city_id).values("pk", "county_name")
    county_list = list(county)
    return JsonResponse(county_list, safe=False)


def get_region_by_county_id(request, county_id):
    county_id = int(county_id)
    region = Region.objects.filter(county=county_id).values("pk", "region_name")
    region_list = list(region)
    return JsonResponse(region_list, safe=False)
