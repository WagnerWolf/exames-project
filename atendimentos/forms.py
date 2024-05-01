from django import forms
from .models import Atendimento, Exame
from django.contrib.auth.models import User

class AtendimentoForm(forms.ModelForm):
    class Meta:
        user = User
        model = Atendimento
        fields = ['codigo','nomePaciente','exames']
        labels = {'codigo':'Código', 'nomePaciente': 'Nome do Paciente'}
        
    #manytomany
    exames = forms.ModelMultipleChoiceField(
        label =  'Selecione os Exames',
        queryset = Exame.objects.all(),
        widget = forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    
    )