# forms.py
from django import forms
from .models import UserCard
from django.contrib.auth.models import User

class UserCardAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")

    class Meta:
        model = UserCard
        fields = ['user', 'image', 'text']
