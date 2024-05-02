"""
URL configuration for exames_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('atendimentos', views.atendimentos, name ='atendimentos'),
    path('atendimentos/<atendimento_id>/', views.atendimento, name ='atendimento'),
    path('atendimentos/<atendimento_id>/edit', views.edit_atendimento, name ='edit_atendimento'),
    path('atendimentos/<atendimento_id>/delete', views.delete_atendimento, name ='delete_atendimento'),
    path('new_atendimento', views.new_atendimento, name ='new_atendimento'),
    path('atendimentos/report', views.report, name ='report'),
    #path('edit_atendimento/<atendimento_id>', views.edit_atendimento, name ='edit_atendimento'),
    #path('delete_atendimento/<atendimento_id>', views.delete_atendimento, name ='delete_atendimento'),
]
