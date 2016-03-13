from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.


def main(request):
    return render(request, 'main/main.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            context = {
                "error": "Username already exists."
            }
            return render(request, 'main/signup.html', context)

        if password1 != password2:
            context = {
                "error":"Password Mismatched",
            }
            return render(request, 'main/signup.html', context)
        password=password1
        user = User.objects.create_user(username,email,password)
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('main:main')

    return render(request, 'main/signup.html')


def sign_in(request):
    if request.user.is_active:
        return redirect('main:main')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect('main:main')

        context = {
            "error": "Invalid Username or Password"
        }
        return render(request, 'main/sign_in.html', context)

    return render(request, 'main/sign_in.html')


def sign_out(request):
    logout(request)
    return redirect('main:main')
