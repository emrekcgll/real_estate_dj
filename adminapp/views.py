from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from django.conf import settings
from django.db import transaction

from adminapp.forms import EstateBuyerForm, EstateOwnerForm, EstateRentForm, EstateRenterForm, RealEstateForm
from adminapp.models import *

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os
import json


def index(request):
    try:
        satilik = get_object_or_404(EstateStatus, estate_status="Satılık")
        kiralik = get_object_or_404(EstateStatus, estate_status="Kiralık")
    except:
        satilik = None
        kiralik = None

    estates_on_sale = RealEstate.objects.filter(estate_status=satilik, estate_buyer=None).count() if satilik else 0
    estates_on_sold = RealEstate.objects.exclude(estate_buyer=None).count() if satilik else 0
    estates_on_rent = RealEstate.objects.filter(estate_status=kiralik, estate_renter=None).count() if satilik else 0
    estates_on_rented = RealEstate.objects.exclude(estate_renter=None).count() if satilik else 0

    context = {"estates_on_sale": estates_on_sale, "estates_on_sold": estates_on_sold,
               "estates_on_rent": estates_on_rent, "estates_on_rented": estates_on_rented}
    return render(request, 'adminapp/index.html', context)


# ESTATE OPERATIONS
def estates(request):
    room_list = RoomCount.objects.all()
    status_list = EstateStatus.objects.all()
    type_list = EstateType.objects.all()

    # Veritabanı sorgusu
    estates = RealEstate.objects.select_related('city', 'county', 'region', 'room_count', 'estate_status').prefetch_related('image_set')
    
    # Görüntüleme sayısı
    view = int(request.GET.get("view", 10))
    view = min(max(view, 10), 30)  # Min 10, max 30 yap

    # Durum filtresi
    status = request.GET.get("status")
    if status != "all" and status is not None:
        estates = estates.filter(estate_status__pk=status)    

    # Tip filtresi
    type = request.GET.get("type")
    if type != "all" and type is not None:
        estates = estates.filter(estate_type__pk=type)

    # Oda Filtresi
    room = request.GET.getlist("room_count")
    if room:
        estates = estates.filter(room_count__pk__in=room)
        
    # Sıralama Filtresi
    sort = request.GET.get("sort")
    if sort == "old-to-new":
        estates = estates.order_by("pk")
    else:
        estates = estates.order_by("-pk")

    # Fiyat Filtresi
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")
    try:
        max_price = int(max_price) if max_price else None
        min_price = int(min_price) if min_price else None
    except ValueError:
        max_price = None
        min_price = None
    if isinstance(max_price, int) or isinstance(min_price, int):
        if max_price and min_price:
            estates = estates.filter(price__gte=float(min_price), price__lte=float(max_price))
        elif max_price:
            estates = estates.filter(price__lte=float(max_price))
        elif min_price:
            estates = estates.filter(price__gte=float(min_price))

    # Metre Filtresi
    max_metre = request.GET.get("max_metre")
    min_metre = request.GET.get("min_metre")
    try:
        max_metre = int(max_metre) if max_metre else None
        min_metre = int(min_metre) if min_metre else None
    except ValueError:
        max_metre = None
        min_metre = None
    if isinstance(max_metre, int) or isinstance(min_metre, int):
        if max_metre and min_metre:
            estates = estates.filter(m2_brut__gte=float(min_metre), m2_brut__lte=float(max_metre))
        elif max_metre:
            estates = estates.filter(m2_brut__lte=float(max_metre))
        elif min_metre:
            estates = estates.filter(m2_brut__gte=float(min_metre))


    estates = [
        {
            "pk": item.pk,
            "title": item.title,
            "city": item.city.city_name,
            "county": item.county.county_name,
            "region": item.region.region_name,
            "room_count": item.room_count.room_count,
            "estate_status": item.estate_status.estate_status,
            "estate_type": item.estate_type.estate_type,
            "price": item.price,
            "image": item.image_set.first(),
        }
        for item in estates
    ]

    paginator = Paginator(estates, view)
    page = request.GET.get("page")
    try:
        data = paginator.page(page)
        page_range = paginator.page_range[max(0, data.number - 5): data.number + 5]
    except PageNotAnInteger:
        data = paginator.page(1)
        page_range = paginator.page_range[:5]
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
        page_range = paginator.page_range[-5:]

    total_estate = paginator.count
    items_per_page = len(data)
    context = {
        "data": data, "page_range": page_range,
        "view": view, "sort": sort, "status": status,
        "total_estate": total_estate,
        "items_per_page": items_per_page,
        
        "status_list": status_list,
        "type_list": type_list,
        "room_list": room_list,
    }
    return render(request, "adminapp/estates.html", context)


def estate_details(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    estate_s = estate.estate_status
    images = Image.objects.filter(real_estate=estate)
    return render(request, "adminapp/estatedetails.html", {"estate": estate,
                                                           "images": images,
                                                           "estate_s": estate_s})


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
                    estate_owner, created = EstateOwner.objects.get_or_create(phone=phone, defaults={"name_surname": name_surname, "phone": phone, "address": address, "identity_number": identity_number})
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
                transaction.set_rollback(True)
                print(f"Hata: {e}")
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
    estates_by_owner = RealEstate.objects.filter(estate_owner=owner).only("pk", "city__city_name", "county__county_name", "region__region_name", "room_count__room_count", "address", "title")\
                                                                    .select_related("city", "county", "region", "room_count").all()
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
    estates_by_renter = RealEstate.objects.filter(estate_renter=renter).only("pk", "city__city_name", "county__county_name", "region__region_name", "room_count__room_count", "address", "title")\
                                                                       .select_related("city", "county", "region", "room_count").first()
    return render(request, "adminapp/renterdetails.html", {"renter": renter, "estates_by_renter": estates_by_renter})


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


# CONTRAT OPERATIONS
def estate_rent_contrats(request):
    contrat = RealEstate.objects.all()
    return render(request, "adminapp/estate_rent_contrats.html")


def estate_rent_contrat_details(request, pk):
    estate_rent_contrat = get_object_or_404(RealEstate, estate_rent_contrat=pk) 
    return render(request, "adminapp/estate_rent_contrat_details.html", 
                  {"estate_rent_contrat": estate_rent_contrat,})


@transaction.atomic
def estate_rent_contrat_create(request, pk):
    try:
        estate = get_object_or_404(RealEstate, pk=pk)
        if request.method == "POST":
            form = EstateRentForm(request.POST)
            if form.is_valid():
                estate_rent_contrat = form.save(commit=False)
                estate_rent_contrat.save()

                estate.estate_rent_contrat = estate_rent_contrat
                estate.save()

                comission = request.POST.get("comission")
                RealEstateAgentCommission.objects.create(
                    user=request.user, estate=estate, comission=comission)

                return redirect("estate_details", pk=estate.pk)
        form = EstateRentForm()
        return render(request, "adminapp/estate_rent_contrat_create.html", {"form": form})
    except Exception as e:
        transaction.set_rollback(True)
        print(f"Hata: {e}")


def estate_rent_contrat_update(request, pk):
    estate_rent_contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == "POST":
        form = EstateRentForm(request.POST, instance=estate_rent_contrat)
        if form.is_valid():
            form.save()
            return redirect("estate_rent_contrats")
    else:
        form = EstateRentForm(instance=estate_rent_contrat)
    return render(request, "adminapp/estate_rent_contrat_update.html", {"form": form})


def estate_rent_contrat_pdf(request, pk):
    estate_rent_contrat = get_object_or_404(RealEstate, estate_rent_contrat=pk)
    pdfmetrics.registerFont(TTFont('ArialUnicode', 'static/arialuni.ttf'))
    buffer = BytesIO()
    para_style = ParagraphStyle(
        name="Normal", wordWrap=True, fontName='ArialUnicode')
    para_style2 = ParagraphStyle(
        name="Normal", wordWrap=True, fontName='ArialUnicode')
    # para_style2 = ParagraphStyle(name="Normal", wordWrap=True, fontName='ArialUnicode', fontSize=12, leading=15)

    styles = getSampleStyleSheet()
    header_style = styles['Title']
    header_style.alignment = 1
    header_style.fontName = 'ArialUnicode'
    header_style.fontSize = 24
    header_style.spaceAfter = 20
    header_style.spaceBefore = 40
    header_text = Paragraph("KİRA SÖZLEŞMESİ", header_style)

    daire_no = Paragraph("Daire Numarasi", para_style)
    daire_no_text = Paragraph(estate_rent_contrat.apartment_number, para_style)
    diskapi_no = Paragraph("Dış Kapı Numarası", para_style)
    diskapi_no_text = Paragraph(
        estate_rent_contrat.exterior_door_number, para_style)
    cadde_sokak = Paragraph("Cadde / Sokak", para_style)
    cadde_sokak_text = Paragraph(estate_rent_contrat.address, para_style)
    mahalle = Paragraph("Daire Numarasi", para_style)
    mahalle_text = Paragraph(
        estate_rent_contrat.region.region_name, para_style)
    semt_il_ilce = Paragraph("Semt / İl / İlce", para_style)
    semt_il_ilce_text = Paragraph(
        f"{estate_rent_contrat.region.region_name} / {estate_rent_contrat.county.county_name} / {estate_rent_contrat.city.city_name}", para_style)
    kiralanan_cinsi = Paragraph("Kiralananın Cinsi", para_style)
    kiralanan_cinsi_text = Paragraph(
        estate_rent_contrat.estate_type.estate_type, para_style)
    kiralayan_ad_soyad = Paragraph("Kiralayanın Adı Soyadı", para_style)
    kiralayan_ad_soyad_text = Paragraph(
        estate_rent_contrat.estate_renter.name_surname, para_style)
    kiralayan_tc = Paragraph("Kiralayanın T.C. Kimlik No", para_style)
    kiralayan_tc_text = Paragraph(
        estate_rent_contrat.estate_renter.identity_number, para_style)
    kiralayan_adres = Paragraph("Kiralayanın Adresi", para_style)
    kiralayan_adres_text = Paragraph(
        estate_rent_contrat.estate_renter.address, para_style)
    kiranin_baslangic_tarihi = Paragraph(
        "Kiranın Başlangıç Tarihi", para_style)
    kiranin_baslangic_tarihi_text = estate_rent_contrat.estate_rent_contrat.contract_start_date
    kiranin_suresi = Paragraph("Kiranın Süresi", para_style)
    kiranin_suresi_text = estate_rent_contrat.estate_rent_contrat.contract_duration
    aylik_kira_bedeli = Paragraph("Aylık Kira Bedeli", para_style)
    aylik_kira_bedeli_text = estate_rent_contrat.estate_rent_contrat.mounth_rental_price
    yillik_kira_bedeli = Paragraph("Yıllık Kira Bedeli", para_style)
    yillik_kira_bedeli_text = estate_rent_contrat.estate_rent_contrat.year_rental_price
    kira_bedelini_ödeme_sekli = Paragraph(
        "Kira Bedelinin Ödeme Şekli", para_style)
    kira_bedelini_ödeme_sekli_text = Paragraph(
        estate_rent_contrat.estate_rent_contrat.rent_payment_method, para_style)
    kiralanani_kullanim_durumu = Paragraph(
        "Kiralananı Kullanım Şekli", para_style)
    kiralanani_kullanim_durumu_text = Paragraph(
        estate_rent_contrat.estate_rent_contrat.how_to_use_the_rented_property, para_style)
    kiralananin_durumu = Paragraph("Kiralananın Durumu", para_style)
    kiralananin_durumu_text = Paragraph(
        estate_rent_contrat.estate_rent_contrat.status_of_the_rented_property, para_style)
    demirbaslar = Paragraph(
        "Kiralananla Birlikte Teslim Edilen Demirbaşlar", para_style)
    demirbaslar_text = Paragraph(
        estate_rent_contrat.estate_rent_contrat.fixtures_delivered_with_the_rental, para_style)

    data = [
        [daire_no, daire_no_text],
        [diskapi_no, diskapi_no_text],
        [cadde_sokak, cadde_sokak_text],
        [mahalle, mahalle_text],
        [semt_il_ilce, semt_il_ilce_text],
        [kiralanan_cinsi, kiralanan_cinsi_text],
        [kiralayan_ad_soyad, kiralayan_ad_soyad_text],
        [kiralayan_tc, kiralayan_tc_text],
        [kiralayan_adres, kiralayan_adres_text],
        [kiranin_baslangic_tarihi, kiranin_baslangic_tarihi_text],
        [kiranin_suresi, str(kiranin_suresi_text)],
        [aylik_kira_bedeli, aylik_kira_bedeli_text],
        [yillik_kira_bedeli, yillik_kira_bedeli_text],
        [kira_bedelini_ödeme_sekli, kira_bedelini_ödeme_sekli_text],
        [kiralanani_kullanim_durumu, kiralanani_kullanim_durumu_text],
        [kiralananin_durumu, kiralananin_durumu_text],
        [demirbaslar, demirbaslar_text]
    ]
    imza = [["Kiraya Veren", "Kefil", "Kiralayan"]]
    table_imza = Table(imza, colWidths=[170, 170, 170])
    table_imza_style = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER')])
    table_imza.setStyle(table_imza_style)

    genel_kosullar_text = Paragraph("GENEL KOŞULLAR", header_style)
    with open('static/genel_kosullar.json', 'r', encoding='utf-8') as f:
        genel_kosullar = json.load(f)
    genel_kosullar = genel_kosullar["genel_kosullar"]

    data2 = []
    for item in genel_kosullar:
        text = Paragraph(item, para_style2)
        data2.append([text])

    table = Table(data, colWidths=[150, 350])
    table2 = Table(data2, colWidths=[500])

    style = TableStyle([('GRID', (0, 0), (-1, -1), 0.1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')])
    style2 = TableStyle([('GRID', (0, 0), (-1, -1), 0.1, colors.black),
                         ('VALIGN', (0, 0), (-1, -1), 'TOP')])

    table.setStyle(style)
    table2.setStyle(style2)

    elements_page1 = [header_text, table, Spacer(1, 3.32*inch), table_imza]
    elements_page2 = [genel_kosullar_text,
                      table2, Spacer(1, 0.92*inch), table_imza]

    doc = SimpleDocTemplate(buffer, pagesize=letter, encoding='utf-8')
    elements = []
    elements.extend(elements_page1)
    elements.append(PageBreak())
    elements.extend(elements_page2)

    doc.build(elements)

    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='kira-kontratı().pdf',
                            content_type='application/pdf; charset=utf-8')
    return response


def estate_rent_contrat_delete(request, pk):
    estate_rent_contrat = get_object_or_404(Contrat, pk=pk)
    estate_rent_contrat.delete()
    return redirect("estate_rent_contrats")


# BUYER OPERATIONS
def buyers(request):
    buyers = EstateBuyer.objects.all()
    return render(request, "adminapp/buyers.html", {"buyers": buyers})


def buyer_details(request, pk):
    buyer = get_object_or_404(EstateBuyer, pk=pk)
    estates_by_buyer = RealEstate.objects.filter(estate_buyer=buyer).only("pk", "city__city_name", "county__county_name", "region__region_name", "room_count__room_count", "address", "title")\
        .select_related("city", "county", "region", "room_count").first()
    return render(request, "adminapp/buyerdetails.html", {"buyer": buyer, "estates_by_buyer": estates_by_buyer})


def buyer_create(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    if request.method == "POST":
        name_surname = request.POST.get("name_surname")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        identity_number = request.POST.get("identity_number")
        estate_buyer = EstateBuyer(
            name_surname=name_surname,
            identity_number=identity_number,
            phone=phone, address=address)
        estate_buyer.save()
        estate.estate_buyer = estate_buyer
        estate.save()
        return redirect("estate_details", pk=estate.pk)
    return render(request, "adminapp/buyercreate.html")


def buyer_update(request, pk):
    estate_pk = request.GET.get("estate_pk")
    estate_buyer = get_object_or_404(EstateBuyer, pk=pk)
    if request.method == "POST":
        form = EstateBuyerForm(request.POST, instance=estate_buyer)
        if form.is_valid():
            form.save()
            if estate_pk:
                return redirect("estate_details", pk=estate_pk)
            else:
                return redirect("buyers")
    else:
        form = EstateBuyerForm(instance=estate_buyer)
    return render(request, "adminapp/buyerupdate.html", {"form": form})


def buyer_delete(request, pk):
    buyer = get_object_or_404(EstateBuyer, pk=pk)
    buyer.delete()
    return redirect("buyers")


# AJAX OPERATIONS
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
