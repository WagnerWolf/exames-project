from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Exame(models.Model):
    mnemonico = models.CharField(max_length=10)
    nomeExame = models.CharField(max_length=100)
    mneapoio = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.mnemonico} {self.nomeExame}"
  
class Atendimento (models.Model):
    """Atendimento, contendo exames e tudo mais"""
    codigo = models.CharField(max_length=12)
    nomePaciente = models.CharField(max_length=200)
    dataAtendimento = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    exames = models.ManyToManyField("Exame")

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

  
class Apoio(models.Model):
    nomeApoio = models.CharField(max_length=200)

    def __str__(self):
        return self.nomeApoio

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14)