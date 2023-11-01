from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "homeapp/index.html")

def h_estates(request):
    return render(request, "homeapp/estates.html")


def h_estate_details(request, pk):
    return render(request, "homeapp/estate_details.html")