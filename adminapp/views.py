from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from numpy import unicode_
from adminapp.forms import EstateBuyerForm, EstateOwnerForm, EstateRentForm, EstateRenterForm, RealEstateForm
from adminapp.models import Contrat, County, EstateBuyer, EstateOwner, EstateRenter, EstateStatus, Image, RealEstate, Region
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.conf import settings
from django.db import transaction


def index(request):
    satilik = get_object_or_404(EstateStatus, estate_status="Satılık")
    kiralik = get_object_or_404(EstateStatus, estate_status="Kiralık")

    estates_on_sale = RealEstate.objects.filter(
        estate_status=satilik, estate_buyer=None).count()
    estates_on_sold = RealEstate.objects.exclude(estate_buyer=None).count()
    estates_on_rent = RealEstate.objects.filter(
        estate_status=kiralik, estate_renter=None).count()
    estates_on_rented = RealEstate.objects.exclude(estate_renter=None).count()

    context = {"estates_on_sale": estates_on_sale, "estates_on_sold": estates_on_sold,
               "estates_on_rent": estates_on_rent, "estates_on_rented": estates_on_rented}
    return render(request, 'adminapp/index.html', context)


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
                                                           "estate_s": estate_s, })


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
def estate_rent_contrat_details(request, pk):
    estate_rent_contrat = get_object_or_404(RealEstate, estate_rent_contrat=pk)
    return render(request, "adminapp/estate_rent_contrat_details.html", {"estate_rent_contrat": estate_rent_contrat})


def estate_rent_contrat_create(request, pk):
    estate = get_object_or_404(RealEstate, pk=pk)
    if request.method == "POST":
        form = EstateRentForm(request.POST)
        if form.is_valid():
            estate_rent_contrat = form.save()
            estate.estate_rent_contrat = estate_rent_contrat
            estate.save()
            return redirect("estate_details", pk=estate.pk)
    form = EstateRentForm()
    return render(request, "adminapp/estate_rent_contrat.html", {"form": form})

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from io import BytesIO
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import RealEstate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def estate_rent_contrat_pdf(request, pk):
    estate_rent_contrat = get_object_or_404(RealEstate, estate_rent_contrat=pk)
    pdfmetrics.registerFont(TTFont('ArialUnicode', 'static/arialuni.ttf'))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, encoding='utf-8')
    para_style = ParagraphStyle(name="Normal", wordWrap=True, fontName='ArialUnicode')

    daire_no = Paragraph("Daire Numarasi", para_style)
    daire_no_text = Paragraph(estate_rent_contrat.apartment_number, para_style)

    diskapi_no = Paragraph("Dış Kapı Numarası", para_style)
    diskapi_no_text = Paragraph(estate_rent_contrat.exterior_door_number, para_style)

    cadde_sokak = Paragraph("Cadde / Sokak", para_style)
    cadde_sokak_text = Paragraph(estate_rent_contrat.address, para_style)

    mahalle = Paragraph("Daire Numarasi", para_style)
    mahalle_text = Paragraph(estate_rent_contrat.region.region_name, para_style)

    semt_il_ilce = Paragraph("Semt / İl / İlce", para_style)
    semt_il_ilce_text = Paragraph(f"{estate_rent_contrat.region.region_name} / {estate_rent_contrat.county.county_name} / {estate_rent_contrat.city.city_name}", para_style)

    kiralanan_cinsi = Paragraph("Kiralananın Cinsi", para_style)
    kiralanan_cinsi_text = Paragraph(estate_rent_contrat.estate_type.estate_type, para_style)

    kiralayan_ad_soyad = Paragraph("Kiralayanın Adı Soyadı", para_style)
    kiralayan_ad_soyad_text = Paragraph(estate_rent_contrat.estate_renter.name_surname, para_style)

    kiralayan_tc = Paragraph("Kiralayanın T.C. Kimlik No", para_style)
    kiralayan_tc_text = Paragraph(estate_rent_contrat.estate_renter.identity_number, para_style)

    kiralayan_adres = Paragraph("Kiralayanın Adresi", para_style)
    kiralayan_adres_text = Paragraph(estate_rent_contrat.estate_renter.address, para_style)

    kiranin_baslangic_tarihi = Paragraph("Kiranın Başlangıç Tarihi", para_style)
    kiranin_baslangic_tarihi_text = estate_rent_contrat.estate_rent_contrat.contract_start_date

    kiranin_suresi = Paragraph("Kiranın Süresi", para_style)
    kiranin_suresi_text = estate_rent_contrat.estate_rent_contrat.contract_duration

    aylik_kira_bedeli = Paragraph("Aylık Kira Bedeli", para_style)
    aylik_kira_bedeli_text = estate_rent_contrat.estate_rent_contrat.mounth_rental_price

    yillik_kira_bedeli = Paragraph("Yıllık Kira Bedeli", para_style)
    yillik_kira_bedeli_text = estate_rent_contrat.estate_rent_contrat.year_rental_price

    kira_bedelini_ödeme_sekli = Paragraph("Kira Bedelinin Ödeme Şekli", para_style)
    kira_bedelini_ödeme_sekli_text = Paragraph(estate_rent_contrat.estate_rent_contrat.rent_payment_method, para_style)

    kiralanani_kullanim_durumu = Paragraph("Kiralananı Kullanım Şekli", para_style)
    kiralanani_kullanim_durumu_text = Paragraph(estate_rent_contrat.estate_rent_contrat.how_to_use_the_rented_property, para_style)

    kiralananin_durumu = Paragraph("Kiralananın Durumu", para_style)
    kiralananin_durumu_text = Paragraph(estate_rent_contrat.estate_rent_contrat.status_of_the_rented_property, para_style)

    demirbaslar = Paragraph("Kiralananla Birlikte Teslim Edilen Demirbaşlar", para_style)
    demirbaslar_text = Paragraph(estate_rent_contrat.estate_rent_contrat.fixtures_delivered_with_the_rental, para_style)

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
    
    # Tabloyu oluşturun
    table = Table(data, colWidths=[150, 350])
    style = TableStyle([('GRID', (0, 0), (-1, -1), 0.1, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')])

    table.setStyle(style)

    # Ana başlık eklemek için bir metin paragrafı oluşturun
    styles = getSampleStyleSheet()
    header_style = styles['Title']
    header_style.alignment = 1
    header_style.fontName = 'ArialUnicode'
    header_style.fontSize = 24
    header_style.spaceAfter = 20
    header_text = Paragraph("Kira Sözleşmesi", header_style)
    
    elements = [header_text, table]
    doc.build(elements)
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='veri.pdf', content_type='application/pdf; charset=utf-8')
    return response


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
    estates = RealEstate.objects.filter(
        estate_renter__isnull=False, estate_status=estate_status).order_by("-created_date")

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
    estates = RealEstate.objects.filter(
        estate_renter=None, estate_status=estate_status).order_by("-created_date")

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
    estates = RealEstate.objects.filter(
        estate_buyer__isnull=False, estate_status=estate_status).order_by("-created_date")

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
    estates = RealEstate.objects.filter(
        estate_buyer=None, estate_status=estate_status).order_by("-created_date")

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
