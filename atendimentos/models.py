from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Exame(models.Model):
    mnemonico = models.CharField(max_length=10)
    nomeExame = models.CharField(max_length=100)
    mneapoio = models.CharField(max_length=10)
    valor = models.FloatField(max_length=10)
    atendimentos = models.ManyToManyField("Atendimento", through="ExameQtd")

    def __str__(self):
        return f"{self.mnemonico} {self.nomeExame}"
  
class Atendimento (models.Model):
    """Atendimento, contendo exames e tudo mais"""
    codigo = models.CharField(max_length=12)
    nomePaciente = models.CharField(max_length=200)
    dataAtendimento = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exames = models.ManyToManyField("Exame", through="ExameQtd")

    def __str__ (self):
        exames = list(self.exames.all())
        ex = []
        for exame in exames:
            ex.append(exame.mnemonico)
        ex = str(ex)
        ex = ex.replace("[","")
        ex = ex.replace("]","")
        ex = ex.replace("'","")
        ex = ex.replace(" ","")
        ex = ex.replace(",",", ")
        #return f"{self.codigo} {self.nomePaciente} {self.usuario} {list(self.exames.all())} {self.dataAtendimento}"
        #return f"Código: {self.codigo} Nome do Paciente: {self.nomePaciente} Usuário: {self.usuario} Exames: {list(self.exames.all())}"
        return ex

  

class ExameQtd(models.Model):
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    atendimento = models.ForeignKey("Atendimento", on_delete=models.CASCADE)
    qtd = models.IntegerField(default=1)
    
    def __str__ (self):
        print(str(self.atendimento.nomePaciente))
        print(str(self.atendimento.codigo))
        print(str(self.atendimento.usuario))
        print(str(self.atendimento.exames.all()))
        print(str(self.qtd))
        print(str(self.atendimento.dataAtendimento))
        return str(self.qtd)