from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', {'message': None})

    return HttpResponseRedirect(reverse('orders:home'))

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("users:index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def register_view(request):
    if request.method == 'GET':
        return render(request, 'users/register.html', {'message': None})
    else:
        username_register = request.POST.get('username_register')
        password_register = request.POST.get('password_register')
        email_register = request.POST.get('email_register')
        try:
            user = User.objects.create_user(username_register, email_register, password_register)
            return HttpResponseRedirect(reverse("users:index"))
        #IntegrityError exception occurs where there is also a user with that username
        except IntegrityError as e:
            return render(request, 'users/register.html', {'message': e.__cause__ })
