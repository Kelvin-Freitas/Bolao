from django.contrib import admin
from .models import Partida,Resultado,Apostas,Rodada
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from bolao.models import Profile

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Partida)
admin.site.register(Resultado)
admin.site.register(Apostas)
admin.site.register(Rodada)