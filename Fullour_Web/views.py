from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import MyUser

from django.http import HttpResponse

def index(request):
    title = 'Home page'
    return HttpResponse(title)

def login(request):
    
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

    

def logout(request):
    logout(request)
    