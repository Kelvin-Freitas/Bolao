from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Rodada(models.Model):
    rodada = models.IntegerField(blank=False,null=True)
    permitirApostas = models.BooleanField(default=True)

    def __str__(self):
        return "Rodada #" + str(self.rodada)
    
    def rodadaNumber(self):
        return str(self.rodada)

class Partida(models.Model):
    rodada = models.ForeignKey(Rodada, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    timeCasa = models.CharField(max_length=30)
    iconTimeCasa = models.CharField(max_length=300, null=True)
    timeVisitante = models.CharField(max_length=30)
    iconTimeVisitante = models.CharField(max_length=300, null=True)
    partidaRealizada = models.BooleanField(default=False)
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
    valor_aposta = models.FloatField(default=5.00)
    aposta_placar_casa = models.IntegerField()
    aposta_placar_vistante = models.IntegerField()
    aposta_vencedor = models.CharField(max_length=30)

    def atualizar(self,userId):
        profile = Profile.objects.get(user=userId)
        profile.credito = profile.credito - 5
        profile.apostou = True
        profile.save()

    def __str__(self):
        return "Aposta em: " + str(self.aposta_vencedor) + " com placar " + str(self.aposta_placar_casa) + " x " + str(self.aposta_placar_vistante)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credito = models.FloatField(default=10.00)
    apostou = models.BooleanField(default=False)
    def get_creditos():
        return self.credito

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()