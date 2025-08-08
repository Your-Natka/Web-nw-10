# pylint: disable=no-member

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Quote, Author, Tag


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class QuoteForm(forms.ModelForm):
    tags = forms.CharField(help_text='Розділіть теги комами')

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
