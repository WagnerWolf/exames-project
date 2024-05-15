from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as authLogin
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from atendimentos.forms import UserInfoForm
from django.contrib import messages

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
        """Cadastro de um novo usuário"""
        if request.method != 'POST':
            form = UserCreationForm()
            form2 = UserInfoForm()            
        else:
            user_data = {
                'username': request.POST.get('username'),
                'password1': request.POST.get('password'),
                'password2': request.POST.get('password_confirm')
            }
            user_info_data = {
                'nome': request.POST.get('fullname'),
                'cpf': request.POST.get('cpf')
            }
            form = UserCreationForm(user_data)
            form2 = UserInfoForm(user_info_data)
            # Processa o formulário preenchido
            if form.is_valid() and form2.is_valid():
                new_user = form.save(commit=False)
                new_user.username = request.POST.get('username')
                new_user.set_password(request.POST.get('password'))
                new_user.save()
                new_userinfo = form2.save(commit=False)
                new_userinfo.user = new_user
                new_userinfo.nome = request.POST.get('fullname')
                new_userinfo.cpf = request.POST.get('cpf')
                new_userinfo.save()
                
                authenticated_user = authenticate(username=new_user.username, password=request.POST['password'])
                authLogin(request, authenticated_user)
                messages.success(request, 'Usuário registrado com sucesso!')
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, 'Por favor, corrija os erros abaixo.')

        context = {'form': form, 'form2': form2}
        return render(request, 'users/register.html', context)
    