from django.contrib import admin

# Register your models here.
from atendimentos.models import Atendimento
from atendimentos.models import Exame

admin.site.register(Atendimento)
admin.site.register(Exame)