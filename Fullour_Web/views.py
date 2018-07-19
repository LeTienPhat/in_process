from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import DeleteView

from .models import MyUser
from .forms import DeleteUserForm

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

@login_required(login_url='/login/')
def index(request):
    title = 'Dashboard'
    #username = request.user.username
    return render(
        request,
        'index.html',
        {'title':title,},
    )

def admin_check(self):
    return self.__class__.objects.filter(view_all=True)

@login_required(login_url='/login/')
@user_passes_test(admin_check)
def users(request):
    title = 'List of users'
    users = MyUser.objects.filter(is_admin=False)
    return render(request, 'users.html', {'title': title, 'users':users})

@login_required(login_url='/login/')
@user_passes_test(admin_check)
def user_detail(request, id):
    try:
        title = MyUser.objects.get(id=id).username
        user_id = MyUser.objects.get(id=id)
    except MyUser.DoesNotExist:
        current_path = request.get_full_path()
        return render(request, '404.html', {'current_path':current_path})
    return render(request, 'user_detail.html', {'title':title, 'user_id':user_id})
'''
@login_required(login_url='/login/')
@user_passes_test(admin_check)
def delete_user(request ,id):
    title = 'Delete user'
    u = get_object_or_404(MyUser, id=id)
    if request.method == 'POST':
        form = DeleteUserForm(request.POST, instance=u)
        if form.is_valid():
            u.delete()
            return redirect('users')
        else:
            messages.error(request, 'User not found')
    return render(request, 'delete_user.html', {'title':title, 'form':form})
'''