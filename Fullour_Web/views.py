from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

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

@login_required(login_url='/login/')
@user_passes_test(lambda u:u.username == 'admin', login_url='/login/')
def users(request):
    title = 'List of users'
    users = MyUser.objects.filter(is_admin=False)
    return render(request, 'user/list_users.html', {'title': title, 'users':users})

@login_required(login_url='/login/')
def user_detail(request, id):
    try:
        title = 'Personal Information Of: %s' % MyUser.objects.get(id=id).username
        user_id = MyUser.objects.get(id=id)
        
        if (request.user.username == 'admin') or (int(id) == int(request.user.id)):
            return render(
                request, 
                'user/user_detail.html', 
                {'title':title, 'user_id':user_id,}
            )
        else:
            title = 'Forbidden'
            current_path = request.get_full_path()
            return render(
                request, 
                'error/forbidden.html', 
                {'title':title,'current_path':current_path}
            )

    except MyUser.DoesNotExist:
        title = 'User Not Found'
        current_path = request.get_full_path()
        return render(
            request, 
            'error/user_not_found.html', 
            {'title':title, 'current_path':current_path}
        )

@login_required(login_url='/login/')
@user_passes_test(lambda u:u.username == 'admin', login_url='/login/')
def delete_user(request, id):
    try:
        title = 'Delete user: %s' % MyUser.objects.get(id=id).username
        user_id = MyUser.objects.get(id=id)
        form = DeleteUserForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                user_id.delete()
                return redirect('users')
    except MyUser.DoesNotExist:
        title = 'User Not Found'
        return render(request, 'error/user_not_found.html', {'title':title})
    return render(
        request, 
        'user/delete_user.html', 
        {'title':title,'user_id':user_id}
    )

@login_required(login_url='/login/')
@user_passes_test(lambda u:u.username == 'admin', login_url='/login/')
def change_permission(request, id):
    title = 'Change permission for %s' % MyUser.objects.get(id=id).username
    user_id = request.POST['id']
    return render(request, '', {'title':title, 'user_id':user_id})

'''
@login_required(login_url='/login/')
@user_passes_test(lambda u:u.view_all, login_url='/login/')
def edit_user(request, id):
    title = 'Edit user: %s' % MyUser.objects.get(id=id).username
    user_id = MyUser.objects.get(id=id)
    try:
        title = 'Edit user: %s' % MyUser.objects.get(id=id).username
    except MyUser.DoesNotExist:
        title = 'User Not Found'
        return render(request, 'errors/user_not_found.html', {'title':title})
    return render(request, 'user/edit_user.html', {'title':title, 'user_id':user_id})
'''
