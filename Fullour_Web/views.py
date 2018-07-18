from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404

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
    #username = request.user.username
    return render(
        request,
        'index.html',
        {'title':title,},
    )

def users(request):
    title = 'List of users'
    users = MyUser.objects.all()
    return render(request, 'users.html', {'title': title, 'users':users})

def user_detail(request, id):
    try:
        title = MyUser.objects.get(id=id).username
        user_id = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        raise Http404('User does not exist')
    return render(request, 'user_detail.html', {'title':title, 'user_id':user_id})