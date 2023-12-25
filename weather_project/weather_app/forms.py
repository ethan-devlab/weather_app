# coding=utf-8
import attrs
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AuthenticationForm(UserCreationForm):
    username = forms.CharField(
        label="帳號 Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="電子郵件 Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label="密碼 Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label="密碼確認 Verify Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # api = forms.CharField(
    #     label="API",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'api'})
    # )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號 Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼 Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    api = forms.CharField(
        label="API",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'api'})
    )

# class LimitedForm(forms.Form):