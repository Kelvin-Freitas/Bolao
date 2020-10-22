from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
# Create your models here.

class Time(models.Model):
	id = models.AutoField(primary_key=True, unique=True)
	nome = models.CharField("nome", max_length=255)
	brasao = models.CharField("brasao", max_length=255)

class Rodada(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rodada = models.IntegerField(blank=False,null=True)
    permitirApostas = models.BooleanField(default=True)

    def __str__(self):
        return "Rodada #" + str(self.rodada)
    
    def rodadaNumber(self):
        return str(self.rodada)

class Partida(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rodada = models.ForeignKey(Rodada, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    timeCasa = models.CharField(max_length=30)
    iconTimeCasa = models.CharField(max_length=300, null=True)
    timeVisitante = models.CharField(max_length=30)
    iconTimeVisitante = models.CharField(max_length=300, null=True)
    partidaRealizada = models.BooleanField(default=False)
    dataPartida = models.DateTimeField(blank=True, null=True)
    premiacao = models.FloatField(default=0.00)
    premiacaoDistribuida = models.BooleanField(default=False)

    def publish(self):
        self.save()
    
    def __str__(self):
        return self.title

class Resultado(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    placarCasa = models.IntegerField() 
    placarVisitante = models.IntegerField()
    vencedorPartida = models.CharField(max_length=30)
    partida = models.OneToOneField(Partida, on_delete=models.SET_NULL, null=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.partida.timeCasa + ' ' + str(self.placarCasa) + ' x ' + str(self.placarVisitante) + ' ' + self.partida.timeVisitante

class Apostas(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aposta_data = models.DateTimeField(default=timezone.now)
    valor_aposta = models.FloatField(default=5.00)
    aposta_placar_casa = models.IntegerField()
    aposta_placar_vistante = models.IntegerField()
    aposta_vencedor = models.CharField(max_length=30)
    partida = models.OneToOneField(Partida, on_delete=models.SET_NULL, null=True)
    

    def atualizar(self,userId):
        profile = Profile.objects.get(user=userId)
        profile.credito = profile.credito - 5
        profile.apostou = True
        profile.save()
        partida = self.partida
        partida.premiacao = partida.premiacao + 5
        partida.save()

    def __str__(self):
        return "Aposta em: " + str(self.aposta_vencedor) + " com placar " + str(self.aposta_placar_casa) + " x " + str(self.aposta_placar_vistante)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credito = models.FloatField(default=10.00)
    apostou = models.BooleanField(default=False)
    def get_creditos(self):
        return self.credito
    def get_ordem(self):
        return self.objects.order_by('credito')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(signals.post_save, sender=Resultado) 
def create_resultado(sender, instance, created, **kwargs):
    apostas = Apostas.objects.filter(partida=Resultado.partida)
    apostasPlacar = apostas.objects.filter(aposta_placar_casa=Resultado.placarCasa,aposta_placar_visitante=placarVisitante)
    partida = Resultado.partida
    partida.partidaRealizada = True
    if(apostasPlacar.count()==1):
        usuario = apostasPlacar.usuario
        usuario.credito = usuario.credito + partida.premiacao
    elif(apostasPlacar.count()>1):
        premio = partida.premiacao
        premio = premio/apostasPlacar.count()
        for aposta in apostasPlacar:
            usuario = aposta.usuario
            usuario.credito = premio
            
    

@receiver(signals.post_save, sender=Rodada) 
def create_resultado(sender, instance, created, **kwargs):
    print("Save method is called")