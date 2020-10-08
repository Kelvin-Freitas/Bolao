from django.contrib import admin
from .models import Partida,Resultado
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bolao.models import Apostador

# Register your models here.

class ApostadorInline(admin.StackedInline):
    model = Apostador
    can_delete = False
    verbose_name_plural = 'apostador'

class UserAdmin(BaseUserAdmin):
    inlines = (ApostadorInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Partida)
admin.site.register(Resultado)