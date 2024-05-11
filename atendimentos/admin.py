from django.contrib import admin

# Register your models here.
from atendimentos.models import Apoio, Atendimento, UserInfo
from atendimentos.models import Exame

admin.site.register(Atendimento)
admin.site.register(Exame)
admin.site.register(UserInfo)
admin.site.register(Apoio)


