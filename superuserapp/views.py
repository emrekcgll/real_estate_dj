from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from adminapp.models import City, County, CustomGroup, CustomUser, EstateStatus, EstateType, FromWho, RealEstate, Region, RoomCount
from superuserapp.forms import EstateStatusForm, EstateTypeForm, FromWhoForm, RoomCountForm
from django.db import transaction
from django.db.models import Q
import io
import csv
from superuserapp.pagging import paginator


def dashboard(request):
    estate_office_count = Group.objects.count()
    member_count = CustomUser.objects.filter(is_member=True).count()
    estate_agent_count = CustomUser.objects.filter(Q(is_manager=True) | Q(is_worker=True)).count()
    context = {"estate_office_count": estate_office_count, "member_count": member_count, "estate_agent_count": estate_agent_count}
    return render(request, "superuserapp/dashboard.html", context)


def estate_list(request):
    room_list = RoomCount.objects.all()
    status_list = EstateStatus.objects.all()
    type_list = EstateType.objects.all()

    # Veritabanı sorgusu
    estates = RealEstate.objects.select_related('city', 'county', 'region', 'room_count', 'estate_status').prefetch_related('image_set')

    # Görüntüleme sayısı
    view = int(request.GET.get("view", 1))
    view = min(max(view, 1), 30)  # Min 10, max 30 yap

    # Sıralama Filtresi
    sort = request.GET.get("sort")
    if sort == "old-to-new":
        estates = estates.order_by("pk")
    else:
        estates = estates.order_by("-pk")

    # Durum filtresi
    status = request.GET.get("status")
    if status != "all" and status is not None:
        estates = estates.filter(estate_status__pk=status)

    # Tip filtresi
    type = request.GET.get("type")
    if type != "all" and type is not None:
        estates = estates.filter(estate_type__pk=type)

    # Oda Filtresi
    room = request.GET.get("room_count")
    if room:
        room_ids = room.split(",")
        estates = estates.filter(room_count__in=room_ids)

    # Dairenin Bulunduğu Kat Filtresi
    min_location_floor = request.GET.get("min_location_floor")
    max_location_floor = request.GET.get("max_location_floor")
    try:
        min_location_floor = int(
            min_location_floor) if min_location_floor else None
        max_location_floor = int(
            max_location_floor) if max_location_floor else None
    except:
        min_location_floor = None
        max_location_floor = None
    if isinstance(max_location_floor, int) or isinstance(min_location_floor, int):
        if max_location_floor and min_location_floor:
            estates = estates.filter(
                location_floor__gte=min_location_floor, location_floor__lte=max_location_floor)
        elif max_location_floor:
            estates = estates.filter(location_floor__lte=max_location_floor)
        elif min_location_floor:
            estates = estates.filter(location_floor__gte=min_location_floor)

    # Bina Yaşı Filtresi
    min_building_years = request.GET.get("min_building_years")
    max_building_years = request.GET.get("max_building_years")
    try:
        min_building_years = int(
            min_building_years) if min_building_years else None
        max_building_years = int(
            max_building_years) if max_building_years else None
    except:
        min_building_years = None
        max_building_years = None
    if isinstance(max_building_years, int) or isinstance(min_building_years, int):
        if max_building_years and min_building_years:
            estates = estates.filter(
                building_years__gte=min_building_years, building_years__lte=max_building_years)
        elif max_building_years:
            estates = estates.filter(building_years__lte=max_building_years)
        elif min_building_years:
            estates = estates.filter(building_years__gte=min_building_years)

    # Fiyat Filtresi
    max_price = request.GET.get("max_price")
    min_price = request.GET.get("min_price")
    try:
        max_price = int(max_price) if max_price else None
        min_price = int(min_price) if min_price else None
    except:
        max_price = None
        min_price = None
    if isinstance(max_price, int) or isinstance(min_price, int):
        if max_price and min_price:
            estates = estates.filter(price__gte=float(
                min_price), price__lte=float(max_price))
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
            estates = estates.filter(m2_brut__gte=float(
                min_metre), m2_brut__lte=float(max_metre))
        elif max_metre:
            estates = estates.filter(m2_brut__lte=float(max_metre))
        elif min_metre:
            estates = estates.filter(m2_brut__gte=float(min_metre))

    search_query = request.GET.get("q")
    if search_query:
        estates = estates.filter(title__icontains=search_query)

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

    context = {
        "sort": sort, "status": status,
        "status_list": status_list,
        "type_list": type_list,
        "room_list": room_list,
    }
    return paginator(request, data=estates, view=view, template_name="superuserapp/estate_list.html", search_query=search_query, **context)



# Admin-Group OP
def estate_agents(request):
    search_query = request.GET.get('q', '')
    admins = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    if search_query:
        admins = admins.filter(Q(username__icontains=search_query) | Q(
            email__icontains=search_query))
    return paginator(request, data=admins, view=10, search_query=search_query, template_name="superuserapp/estate_agents.html")


def get_manager(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    context = {"user": user}
    return render(request, "superuserapp/get_manager.html", user)


@transaction.atomic
def create_manager(request):
    if request.method == "POST":
        response = request.POST

        username = response.get("username").strip()
        email = response.get("email").strip()
        password = response.get("password")
        repassword = response.get("repassword")
        first_name = response.get("first-name").strip()
        last_name = response.get("last-name")
        phone = response.get("phone")
        bio = response.get("bio")
        image = response.get("image")

        group_name = response.get("group_name").strip()
        group_phone = response.get("group_phone").strip()
        group_description = response.get("group_description").strip()
        group_location = response.get("group_location").strip()
        group_image = response.get("group_image").strip()

        print(request.POST)

        if not password == repassword:
            messages.error(request, 'Girdiğiniz parolalar eşleşmiyor.')
        else:
            has_uppercase = any(char.isupper() for char in password)
            has_lowercase = any(char.islower() for char in password)
            has_digit = any(char.isdigit() for char in password)

            if not (len(password) > 7 and has_uppercase and has_lowercase and has_digit):
                messages.error(request, 'Parolanız en az bir büyük harf, bir küçük harf, ve en az bir adet rakam içermelidir.')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Girdiğiniz email adresi ile daha önce üyelik oluşturulmuştur. Lütfen farklı bir email adresi ile yeniden deneyin.')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Girdiğiniz username ile daha önce üyelik oluşturulmuştur. Lütfen farklı bir username ile yeniden deneyin.')
                else:
                    user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                          first_name=first_name, last_name=last_name,
                                                          is_active=True, is_staff=False, is_superuser=False,
                                                          is_member=False, is_manager=True, is_worker=False,
                                                          phone=phone, bio=bio, image=image)
                    group_name, created = CustomGroup.objects.get_or_create(name=group_name, phone=group_phone,
                                                                            description=group_description,
                                                                            location=group_location,
                                                                            image=group_image)
                    user.groups.add(group_name)
                    user.save()
                    messages.success(request, 'Emlak Ofisi ve Yöneticisi başarı ile oluşturuldu.')
                    return redirect("estate_agents")
    return render(request, "superuserapp/create_manager.html")




# Estate Office OP
def estate_offices(request):
    search_query = request.GET.get('q', '')
    groups = Group.objects.all()
    if search_query:
        groups = groups.filter(name__icontains=search_query)
    return paginator(request, data=groups, view=10, search_query=search_query, template_name="superuserapp/estate_offices.html")


def group_details(request, pk):
    group = get_object_or_404(CustomGroup, pk=pk)
    group_users = group.members.all()

    context = {"group": group, "group_users": group_users}
    return render(request, "superuserapp/group_details.html", context)


@transaction.atomic
def create_group(request):
    if request.method == "POST":
        response = request.POST

        group_name = response.get("group_name").strip()
        group_phone = response.get("group_phone").strip()
        group_description = response.get("group_description").strip()
        group_location = response.get("group_location").strip()
        group_image = response.get("group_image").strip()

        group_name, created = CustomGroup.objects.get_or_create(name=group_name, phone=group_phone,
                                                                description=group_description,
                                                                location=group_location,
                                                                image=group_image)
        if created:
            return redirect("group_detail", pk=group_name.pk)
    return render(request, "superuserapp/create_admin.html")


@transaction.atomic
def update_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        group.name = group_name
        group.save()
        messages.success(request, 'Emlak dükkan ismi başarı ile güncellendi.')
        return redirect('group_detail', pk=group.pk)
    return render(request, "superuserapp/update_group.html")


@transaction.atomic
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_users = group.members.all()
    group_users.delete()
    group.delete()
    return redirect("estate_offices")



# Import OP
def import_operations(request):
    return render(request, "superuserapp/importoperations.html")


def import_address_data(request):
    if request.method == "POST":
        csv_file = request.FILES.get("file")
        if csv_file:
            if csv_file.name.endswith(".csv"):
                csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    city_name_csv = row[1].strip().title()
                    county_name_csv = row[2].strip().title()
                    region_name_csv = row[3].strip().title()
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
                    messages.success(request, "Veriler başarıyla veritabanına kaydedildi.")
            else:
                messages.error(request, "Lütfen CSV uzantılı dosya giriniz.")
        else:
            messages.error(request, "Lütfen bir dosya yükleyeniniz.")
    return redirect('import_operations')


@transaction.atomic
def default_value(request):
    estate_t = EstateType.objects
    estate_t.get_or_create(estate_type="Daire")
    estate_t.get_or_create(estate_type="Villa")
    estate_t.get_or_create(estate_type="Müstakil")
    estate_t.get_or_create(estate_type="Doublex")
    estate_t.get_or_create(estate_type="Triplex")

    estate_s = EstateStatus.objects
    estate_s.get_or_create(estate_status="Satılık")
    estate_s.get_or_create(estate_status="Kiralık")

    from_w = FromWho.objects
    from_w.get_or_create(from_who="Emlakcıdan")
    from_w.get_or_create(from_who="Sahibinden")

    room_c = RoomCount.objects
    room_c.get_or_create(room_count="1+0")
    room_c.get_or_create(room_count="1+1")
    room_c.get_or_create(room_count="2+0")
    room_c.get_or_create(room_count="2+1")
    room_c.get_or_create(room_count="2+2")
    room_c.get_or_create(room_count="3+1")
    room_c.get_or_create(room_count="4+1")
    room_c.get_or_create(room_count="4+2")
    room_c.get_or_create(room_count="5+1")
    room_c.get_or_create(room_count="5+2")
    room_c.get_or_create(room_count="5+3")
    room_c.get_or_create(room_count="6+2")
    messages.success(request, "Değerler veritabanında başarıyla oluşturuldu.")
    return redirect("import_operations")



# List OP
def show_estate_type(request):
    estate_types = EstateType.objects.all()
    data = []
    for i in estate_types:
        data.append({
            "pk": i.pk,
            "estate_type": i.estate_type
        })
    response = {"data": data}
    return JsonResponse(response)


def show_estate_status(request):
    estate_status = EstateStatus.objects.all()
    data = []
    for i in estate_status:
        data.append({
            "pk": i.pk,
            "estate_status": i.estate_status
        })
    response = {"data": data}
    return JsonResponse(response)


def show_from_who(request):
    from_whos = FromWho.objects.all()
    data = []
    for i in from_whos:
        data.append({
            "pk": i.pk,
            "from_who": i.from_who
        })
    response = {"data": data}
    return JsonResponse(response)


def show_room_count(request):
    room_counts = RoomCount.objects.all()
    data = []
    for i in room_counts:
        data.append({
            "pk": i.pk,
            "room_count": i.room_count
        })
    response = {"data": data}
    return JsonResponse(response)



# Create OP
def create_estate_type(request):
    if request.method == "POST":
        form = EstateTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateTypeForm()
    return render(request, "superuserapp/create_estate_type.html", {"form": form})


def create_estate_status(request):
    if request.method == "POST":
        form = EstateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateStatusForm()
    return render(request, "superuserapp/create_estate_status.html", {"form": form})


def create_from_who(request):
    if request.method == "POST":
        form = FromWhoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = FromWhoForm()
    return render(request, "superuserapp/create_from_who.html", {"form": form})


def create_room_count(request):
    if request.method == "POST":
        form = RoomCountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = RoomCountForm()
    return render(request, "superuserapp/create_room_count.html", {"form": form})



# Delete OP
def delete_estate_type(request, pk):
    value = get_object_or_404(EstateType, pk=pk)
    value.delete()
    messages.success(request, "Deleted successfully.")
    return redirect("create_estate_type")


def delete_estate_status(request, pk):
    value = get_object_or_404(EstateStatus, pk=pk)
    value.delete()
    messages.success(request, "Deleted successfully.")
    return redirect("create_estate_status")


def delete_from_who(request, pk):
    value = get_object_or_404(FromWho, pk=pk)
    value.delete()
    messages.success(request, "Deleted successfully.")
    return redirect("create_from_who")


def delete_room_count(request, pk):
    value = get_object_or_404(RoomCount, pk=pk)
    value.delete()
    messages.success(request, "Deleted successfully.")
    return redirect("create_room_count")



# Update OP
def update_estate_type(request, pk):
    value = get_object_or_404(EstateType, pk=pk)
    if request.method == "POST":
        form = EstateTypeForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateTypeForm(instance=value)
    return render(request, "superuserapp/update_estate_type.html", {"form": form})


def update_estate_status(request, pk):
    value = get_object_or_404(EstateStatus, pk=pk)
    if request.method == "POST":
        form = EstateStatusForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = EstateStatusForm(instance=value)
    return render(request, "superuserapp/update_estate_status.html", {"form": form})


def update_from_who(request, pk):
    value = get_object_or_404(FromWho, pk=pk)
    if request.method == "POST":
        form = FromWhoForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = FromWhoForm(instance=value)
    return render(request, "superuserapp/update_from_who.html", {"form": form})


def update_room_count(request, pk):
    value = get_object_or_404(RoomCount, pk=pk)
    if request.method == "POST":
        form = RoomCountForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated successfully.")
        else:
            messages.error(request, "Something went wrong.")
    form = RoomCountForm(instance=value)
    return render(request, "superuserapp/update_room_count.html", {"form": form})
