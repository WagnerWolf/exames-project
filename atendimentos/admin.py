from django.contrib import admin

# Register your models here.
from atendimentos.models import Atendimento
from atendimentos.models import Exame
from atendimentos.models import ExameQtd

admin.site.register(Atendimento)
admin.site.register(Exame)



class ExamesQtdAdmin(admin.ModelAdmin):
    class Meta:
        model = ExameQtd

admin.site.register(ExameQtd,ExamesQtdAdmin)