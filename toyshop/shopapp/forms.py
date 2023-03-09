import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError
from .models import Subscribers, Review, Basket


class SubscribersForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['name','email','tell']
        labels = {
            'name': ('Имя'),
            'email': ('Почта'),
            'tell': ('Телефон'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Email'}),
            'tell': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '89995554433'}),
        }


#Форма регистрации пользователя
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Подтверждение пароля',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password1','email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-input'}),
            'password1': forms.TextInput(attrs={'class': 'form-input'}),
            'password2': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }

#Форма авторизации пользователя
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-input'}))
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-input'}),
            'password': forms.TextInput(attrs={'class': 'form-input'}),
        }


#Форма отзыв о товаре
class FormReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewText']
        labels = {
            'reviewText': ('Отзыв о товаре'),
        }
        widgets = {
            'reviewText': forms.Textarea(attrs={'class': 'text_area_rew','placeholder':'Ваш отзыв о товаре'}),
        }

#Форма с кнопкой для добавления товара в корзину
class BasketForm(forms.Form):
    countProduct = forms.CharField(widget=forms.NumberInput())
