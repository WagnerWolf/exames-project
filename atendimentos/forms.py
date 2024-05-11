from django import forms
from .models import Atendimento, Exame, UserInfo
from django.contrib.auth.models import User
from validate_docbr import CPF

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
    


class UserInfoForm(forms.ModelForm):
    class Meta:
        user = User
        model = UserInfo
        fields = ['nome','cpf']
        labels = {'nome': 'Nome Completo do Usuário', 'cpf': 'CPF'}

    def clean_cpf(self):
        cpfv = CPF()
        cpf = self.cleaned_data['cpf']

        
        if cpfv.validate(cpf) is False:
            raise forms.ValidationError("CPF Inválido")
        return cpf
    