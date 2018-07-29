from django import forms
from .models import MyUser

class EditUserPermissionForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('view_all',)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        exclude = ('id','username','view_all', 'is_admin',)

class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('id',)