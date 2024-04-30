from django import forms
from .models import Atendimento
from django.contrib.auth.models import User

class AtendimentoForm(forms.ModelForm):
    class Meta:
        user = User
        model = Atendimento
        fields = ['codigo','nomePaciente','exames']
        labels = {'codigo':'Código', 'nomePaciente': 'Nome do Paciente', 'exames':'Selecione os Exames'}