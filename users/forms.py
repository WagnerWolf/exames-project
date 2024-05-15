# from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=30)
    senha = forms.CharField(max_length=30, widget=forms.PasswordInput)


    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('usuario')
        if not(nome.isalnum()):
            raise ValidationError('O nome de usuário não pode conter caracteres especiais')
        