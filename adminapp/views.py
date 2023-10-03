from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from adminapp.forms import EstateOwnerForm, EstateRenterForm, RealEstateForm
from adminapp.models import County, EstateOwner, EstateRenter, EstateStatus, Image, RealEstate, Region
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.conf import settings
from django.db import transaction


def index(request):
    return render(request, 'adminapp/index.html')


# ESTATE OPERATIONS
def estates(request):
    return render(request, "adminapp/estates.html")

def estates_on_sale(request):
    return render(request, "adminapp/estates_on_sale.html")

def estates_on_sold(request): 
    return render(request, "adminapp/estates_on_sold.html")

def estates_on_rent(request): 
    return render(request, "adminapp/estates_on_rent.html")

def estates_on_rented(request):
    return render(request, "adminapp/estates_on_rented.html")


def estate_details(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    estate_s = estate.estate_status
    images = Image.objects.filter(real_estate=estate)
    return render(request, "adminapp/estatedetails.html", {"estate": estate,
                                                           "images": images,
                                                           "estate_s": estate_s,})


@transaction.atomic
def estate_create(request):
    if request.method == "POST":
        form = RealEstateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = form.save(commit=False)

                name_surname = request.POST.get("name_surname")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                identity_number = request.POST.get("identity_number")

                if name_surname != "":
                    estate_owner, created = EstateOwner.objects.get_or_create(phone=phone, defaults={
                                                                              "name_surname": name_surname, "phone": phone, "address": address, "identity_number": identity_number})
                    estate_owner_instance = get_object_or_404(
                        EstateOwner, pk=estate_owner.pk)
                    data.estate_owner = estate_owner_instance

                county_id = request.POST.get("county")
                region_id = request.POST.get("region")
                county_instance = get_object_or_404(County, pk=county_id)
                region_instance = get_object_or_404(Region, pk=region_id)

                data.county = county_instance
                data.region = region_instance
                data.save()

                estate_instance = get_object_or_404(RealEstate, pk=data.pk)
                files = request.FILES.getlist("image")
                for image in files:
                    Image.objects.create(
                        real_estate=estate_instance, image=image)

                return redirect("estates")
            except Exception as e:
                # Herhangi bir hata durumunda işlemi geri al
                transaction.set_rollback(True)
                print(f"Hata: {e}")
                return redirect("estates")
    else:
        form = RealEstateForm()

    response = {"form": form}
    return render(request, "adminapp/estatecreate.html", response)


@transaction.atomic
def estate_delete(request, pk):
    try:
        real_estate = get_object_or_404(RealEstate, pk=pk)
        images = Image.objects.filter(real_estate=real_estate)
        for image in images:
            os.remove(os.path.join(settings.MEDIA_ROOT, image.image.name))
        images.delete()
        real_estate.delete()
        return redirect("estates")
    except Exception as e:
        transaction.set_rollback(True)
        print(f"Hata: {e}")
        return redirect("estates")


def estate_update(request, pk):
    real_estate = get_object_or_404(RealEstate, pk=pk)
    estate_owner = real_estate.estate_owner.pk if real_estate.estate_owner else None
    images = Image.objects.filter(real_estate=real_estate)
    if request.method == "POST":
        form = RealEstateForm(request.POST, instance=real_estate)
        if form.is_valid():
            data = form.save(commit=False)

            county_id = request.POST.get("county")
            region_id = request.POST.get("region")
            county_instance = get_object_or_404(County, pk=county_id)
            region_instance = get_object_or_404(Region, pk=region_id)
            estate_owner_instance = get_object_or_404(
                EstateOwner, pk=estate_owner) if estate_owner else None

            data.county = county_instance
            data.region = region_instance
            data.estate_owner = estate_owner_instance

            data.save()
            return redirect("estate_details", pk=real_estate.pk)
    else:
        form = RealEstateForm(instance=real_estate)
    return render(request, "adminapp/estateupdate.html", {"form": form, "images": images})


# OWNER OPERATIONS
def owners(request):
    owner = EstateOwner.objects.all()
    return render(request, "adminapp/owners.html", {"owner": owner})


def owner_details(request, pk):
    owner = get_object_or_404(EstateOwner, pk=pk)
    estates_by_owner = RealEstate.objects.filter(estate_owner=owner).values("pk","city","county","region","address","room_count","title").all()
    return render(request, "adminapp/ownerdetails.html", {"owner": owner, "estates_by_owner": estates_by_owner})


def owner_create(request):
    if request.method == "POST":
        form = EstateOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("owners")
    else:
        form = EstateOwnerForm()
    return render(request, "adminapp/ownercreate.html", {"form": form})


def owner_update(request, pk):
    estate_pk = request.GET.get("estate_pk")
    estate_owner = get_object_or_404(EstateOwner, pk=pk)
    if request.method == "POST":
        form = EstateOwnerForm(request.POST, instance=estate_owner)
        if form.is_valid():
            form.save()
            if estate_pk:
                return redirect("estate_details", pk=estate_pk)
            else:
                return redirect("owners")
    else:
        form = EstateOwnerForm(instance=estate_owner)
    return render(request, "adminapp/ownerupdate.html", {"form": form})


def owner_delete(request, pk):
    owner = get_object_or_404(EstateOwner, pk=pk)
    owner.delete()
    return redirect("owners")


# RENTER OPERATIONS
def renters(request):
    renters = EstateRenter.objects.all()
    return render(request, "adminapp/renters.html", {"renters": renters})


def renter_details(request, pk):
    renter = get_object_or_404(EstateRenter, pk=pk)
    return render(request, "adminapp/renterdetails.html", {"renter": renter})


def renter_create(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    if request.method == "POST":
        name_surname = request.POST.get("name_surname")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        identity_number = request.POST.get("identity_number")
        estate_renter = EstateRenter(
            name_surname=name_surname,
            identity_number=identity_number,
            phone=phone, address=address)
        estate_renter.save()
        estate.estate_renter = estate_renter 
        estate.save()
        return redirect("estate_details", pk=estate.pk)
    return render(request, "adminapp/rentercreate.html")


def renter_update(request, pk):
    estate_pk = request.GET.get("estate_pk")
    estate_renter = get_object_or_404(EstateRenter, pk=pk)
    if request.method == "POST":
        form = EstateRenterForm(request.POST, instance=estate_renter)
        if form.is_valid():
            form.save()
            if estate_pk:
                return redirect("estate_details", pk=estate_pk)
            else:
                return redirect("renters")
    else:
        form = EstateOwnerForm(instance=estate_renter)
    return render(request, "adminapp/renterupdate.html", {"form": form})


def renter_delete(request, pk):
    renter = get_object_or_404(EstateRenter, pk=pk)
    renter.delete()
    return redirect("renters")


# AJAX OPERATIONS
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


def estates_on_rented_list_ajax(request):
    estate_status = get_object_or_404(EstateStatus, estate_status="Kiralık")
    # DataTables'ın çizim numarasını alın
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))  # Başlangıç indeksi
    # Sayfa başına gösterilecek öğe sayısı
    length = int(request.GET.get('length', 25))
    search_term = request.GET.get('search[value]')  # Arama terimini alın

    # Tüm emlakları sıralama ve arama terimine göre filtreleme
    estates = RealEstate.objects.filter(estate_renter__isnull=False, estate_status=estate_status).order_by("-created_date")

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


def estates_on_rent_list_ajax(request):
    estate_status = get_object_or_404(EstateStatus, estate_status="Kiralık")
    # DataTables'ın çizim numarasını alın
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))  # Başlangıç indeksi
    # Sayfa başına gösterilecek öğe sayısı
    length = int(request.GET.get('length', 25))
    search_term = request.GET.get('search[value]')  # Arama terimini alın

    # Tüm emlakları sıralama ve arama terimine göre filtreleme
    estates = RealEstate.objects.filter(estate_renter=None, estate_status=estate_status).order_by("-created_date")

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


def estates_on_sold_list_ajax(request):
    estate_status = get_object_or_404(EstateStatus, estate_status="Satılık")
    # DataTables'ın çizim numarasını alın
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))  # Başlangıç indeksi
    # Sayfa başına gösterilecek öğe sayısı
    length = int(request.GET.get('length', 25))
    search_term = request.GET.get('search[value]')  # Arama terimini alın

    # Tüm emlakları sıralama ve arama terimine göre filtreleme
    estates = RealEstate.objects.filter(estate_renter__isnull=False, estate_status=estate_status).order_by("-created_date")

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


def estates_on_sale_list_ajax(request):
    estate_status = get_object_or_404(EstateStatus, estate_status="Satılık")
    # DataTables'ın çizim numarasını alın
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))  # Başlangıç indeksi
    # Sayfa başına gösterilecek öğe sayısı
    length = int(request.GET.get('length', 25))
    search_term = request.GET.get('search[value]')  # Arama terimini alın

    # Tüm emlakları sıralama ve arama terimine göre filtreleme
    estates = RealEstate.objects.filter(estate_renter=None, estate_status=estate_status).order_by("-created_date")

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
