"""
Import required libraries for forms
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import CustomUser, UserProfile


class UserRegisterForm(UserCreationForm):
    """Form for registering new users.
    Extends Django's UserCreationForm and adds an email field
    """
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
        """
        Class to specifying the model and its fields
        """
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    """Form for logging in existing users.
    Extends Django's AuthenticationForm and changes the username field to an email field
    """
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


class ProfileForm(forms.ModelForm):
    """Form for editing user profiles"""
    class Meta:
        """
        Class to specifying the model and its fields
        """
        model = UserProfile
        fields = ('first_name', 'second_name', 'country', 'city', 'street', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EmailForm(forms.ModelForm):
    """Form for editing a user's email"""
    class Meta:
        """
        Class to specifying the model and its fields
        """
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
