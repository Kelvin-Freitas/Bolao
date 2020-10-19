from django.contrib import admin

from sistema.models import Apostador, Aposta, Selecao, Partida, Bolao

# Register your models here.

admin.site.register(Apostador)
admin.site.register(Aposta)
admin.site.register(Selecao)
admin.site.register(Partida)
admin.site.register(Bolao)