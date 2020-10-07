from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Partida(models.Model):
    title = models.CharField(max_length=200)
    timeCasa = models.CharField(max_length=30)
    timeVisitante = models.CharField(max_length=30)
    partidaRealizada = models.BooleanField()
    dataPartida = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.save()
    
    def __str__(self):
        return self.title

class Resultado(models.Model):
    placarCasa = models.IntegerField() 
    placarVisitante = models.IntegerField()
    vencedorPartida = models.CharField(max_length=30)
    partida = models.OneToOneField(Partida, on_delete=models.SET_NULL, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.partida.timeCasa + ' ' + str(self.placarCasa) + ' x ' + str(self.placarVisitante) + ' ' + self.partida.timeVisitante

class Apostas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aposta_data = models.DateTimeField(default=timezone.now)
    valor_aposta = models.FloatField(5.00)
    aposta_placar_casa = models.IntegerField()
    aposta_placar_vistante = models.IntegerField()
    aposta_vencedor = models.CharField(max_length=30)

    def __str__(self):
        return "Aposta em: " + self.aposta_vencedor + "com placar " + self.aposta_placar_casa + " x " + self.aposta_placar_vistante

class UserProfile(models.Model):
    credito = models.FloatField(default=10.00)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)