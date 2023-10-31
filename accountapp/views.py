from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


def account_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
    return render(request, 'accountapp/login.html')


def account_register(request):
    if request.method == "POST":
        response = request.POST

        username = response.get("username")
        email = response.get("email")
        password = response.get("password")
        repassword = response.get("repassword")
        first_name = response.get("first-name")
        last_name = response.get("last-name")
    
        if not password == repassword:
            messages.error(request, 'Girdiğiniz parolalar eşleşmiyor.')

            has_uppercase = any(char.isupper() for char in password)
            has_lowercase = any(char.islower() for char in password)
            has_digit = any(char.isdigit() for char in password)

            if not (len(password) > 7 and has_uppercase and has_lowercase and has_digit):
                messages.error(request, 'Parolanız en az bir büyük harf, bir küçük harf, ve en az bir adet rakam içermelidir.')

                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Girdiğiniz email adresi ile daha önce üyelik oluşturulmuştur. Lütfen farklı bir email adresi ile yeniden deneyin.')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Girdiğiniz username ile daha önce üyelik oluşturulmuştur. Lütfen farklı bir username ile yeniden deneyin.')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, 
                                                    first_name=first_name, last_name=last_name, 
                                                    is_active=False, is_staff=False, is_superuser=False)
                    user.save()
                    messages.success(request, 'Hesabınız başarı ile oluşturuldu. Mail adresinizi onayladıktan sonra giriş yapabilirsiniz.')
