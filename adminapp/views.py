from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from adminapp.forms import RealEstateForm
from adminapp.models import County, Image, RealEstate, Region
from django.core.paginator import Paginator
from django.db.models import Q
import timeit


def index(request):
    return render(request, 'adminapp/index.html')


def estates(request):
    return render(request, "adminapp/estates.html")


def estate_details(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    images = Image.objects.filter(real_estate=estate)
    return render(request, "adminapp/estate_details.html", {"estate": estate, "images": images})


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
    # DataTables'ın çizim numarasını alın
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))  # Başlangıç indeksi
    # Sayfa başına gösterilecek öğe sayısı
    length = int(request.GET.get('length', 25))
    search_term = request.GET.get('search[value]')  # Arama terimini alın

    # Tüm emlakları sıralama ve arama terimine göre filtreleme
    estates = RealEstate.objects.all().order_by("-created_date")

    if search_term:
        # Eğer bir arama terimi varsa, sorguyu oluşturun
        query = Q(title__icontains=search_term) | Q(city__city_name__icontains=search_term) | Q(county__county_name__icontains=search_term) | Q(
            region__region_name__icontains=search_term) | Q(room_count__room_count__icontains=search_term)
        estates = estates.filter(query)

    total_records = estates.count()

    # Sayfalama işlemini yapın
    paginator = Paginator(estates, length)
    # Start değerine göre doğru sayfayı alın
    page = paginator.page(start // length + 1)

    data = []
    for estate in page:
        image = Image.objects.filter(real_estate=estate.pk).first()
        data.append({
            "pk": estate.pk,
            "image": image.image.url,
            "title": estate.title,
            "city": estate.city.city_name,
            "county": estate.county.county_name,
            "region": estate.region.region_name,
            "room_count": estate.room_count.room_count,
        })

    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)


def get_county_by_city_id(request, city_id):
    city_id = int(city_id)
    county = County.objects.filter(city=city_id).values("pk", "county_name")
    county_list = list(county)
    return JsonResponse(county_list, safe=False)


def get_region_by_county_id(request, county_id):
    county_id = int(county_id)
    region = Region.objects.filter(
        county=county_id).values("pk", "region_name")
    region_list = list(region)
    return JsonResponse(region_list, safe=False)
