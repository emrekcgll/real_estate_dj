from django.http import JsonResponse
from django.shortcuts import render
from adminapp.forms import RealEstateForm
from adminapp.models import RealEstate

# Create your views here.


def index(request):
    return render(request, 'adminapp/index.html')


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
