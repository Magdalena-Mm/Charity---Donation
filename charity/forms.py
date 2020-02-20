from django import forms
from .models import *


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
