from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'name@example.com'}
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'name@example.com'}
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
