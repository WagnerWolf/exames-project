from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as authLogin
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        error = False
        if request.method != 'POST':
            form = LoginForm()
        else:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = request.POST.get('usuario')
                password = request.POST.get('senha')
                user = authenticate(username=username, password=password)
                if user:
                    authLogin(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    error = True
        context = {'form': form, 'error':error}
        return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    else:
        """cadastro de um novo usuário"""
        if request.method != 'POST':
            form = UserCreationForm()
        else:
            form = UserCreationForm(data=request.POST)
            #processa o formulario preenchido
            if form.is_valid():
                new_user = form.save()
                #faz o login e redireciona para a pagina inicial
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
                authLogin(request,authenticated_user)
                return HttpResponseRedirect(reverse('index'))
        context = {'form': form}
        return render(request, 'users/register.html', context)