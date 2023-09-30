from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


def account_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
    return render(request, 'accountapp/login.html')