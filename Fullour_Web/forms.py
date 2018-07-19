from django import forms
from .models import MyUser

class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = []