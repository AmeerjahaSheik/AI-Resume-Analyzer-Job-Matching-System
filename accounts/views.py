from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("analyzer:dashboard")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("analyzer:dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")