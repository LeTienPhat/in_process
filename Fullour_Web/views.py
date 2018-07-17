from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import MyUser

from django.http import HttpResponse

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Wrong username or password')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login/')
def index(request):
    title = 'Dashboard'
    return render(request, 'index.html', {'title':title})
