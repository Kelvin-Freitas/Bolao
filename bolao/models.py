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
    def __str__(self):
        return self.nome

class Rodada(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rodada = models.IntegerField(blank=False,null=True)
    permitirApostas = models.BooleanField(default=True)

    def __str__(self):
        return "Rodada #" + str(self.rodada)
    
    def rodadaNumber(self):
        return str(self.rodada)

class Partida(models.Model):
    id = models.AutoField(primary_key=True)
    rodada = models.ForeignKey(Rodada, on_delete=models.CASCADE,null=True)
    timeCasa = models.ForeignKey(Time, on_delete=models.CASCADE,null=False, related_name='partida_timecasa')
    timeVisitante = models.ForeignKey(Time, on_delete=models.CASCADE,null=False, related_name='partida_timevisitante')
    title = models.CharField(max_length=200)
    dataPartida = models.DateTimeField(blank=True, null=True)
    premiacao = models.FloatField(default=0.00)
    partidaRealizada = models.BooleanField(default=False)
    premiacaoDistribuida = models.BooleanField(default=False)

    def publish(self):
        self.save()
    
    def __str__(self):
        return self.title

class Resultado(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    vencedorPartida = models.ForeignKey(Time, on_delete=models.CASCADE,null=True)
    placarCasa = models.IntegerField() 
    placarVisitante = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.partida.timeCasa.nome + ' ' + str(self.placarCasa) + ' x ' + str(self.placarVisitante) + ' ' + self.partida.timeVisitante.nome

class Apostas(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aposta_data = models.DateTimeField(default=timezone.now)
    valor_aposta = models.FloatField(default=5.00)
    aposta_placar_casa = models.IntegerField()
    aposta_placar_vistante = models.IntegerField()
    aposta_vencedor = models.ForeignKey(Time, on_delete=models.CASCADE,null=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    

    def atualizar(self,userId):
        profile = Profile.objects.get(user=userId)
        profile.credito = profile.credito - 5
        profile.apostou = True
        profile.save()
        partida = self.partida
        partida.premiacao = partida.premiacao + 5
        partida.save()

    def __str__(self):
        return "Apostou em: " + str(self.aposta_vencedor.nome) + " com placar: " + str(self.aposta_placar_casa) + " x " + str(self.aposta_placar_vistante)

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
    partida = Partida.objects.get(id=instance.partida.id)
    partida.partidaRealizada = True
    rodada = Rodada.objects.get(id=partida.rodada.id)
    apostas = Apostas.objects.filter(partida=instance.partida.id,aposta_placar_casa=instance.placarCasa,aposta_placar_vistante=instance.placarVisitante)
    if(apostas.count()==1):
        for aposta in apostas:
            usuario = User.objects.get(id=aposta.usuario.id)
            usuario.profile.credito = usuario.profile.credito + partida.premiacao
            usuario.profile.apostou = False
            usuario.save()
    elif(apostas.count() > 1):
        premio = partida.premiacao
        premio = premio / apostas.count()
        for aposta in apostas:
            usuario = User.objects.get(id=aposta.usuario.id)
            usuario.profile.credito = usuario.profile.credito + premio
            usuario.profile.apostou = False
            usuario.save()
    else:
        apostas = Apostas.objects.filter(partida=instance.partida.id,aposta_vencedor=instance.vencedorPartida)
        if(apostas.count()==1):
            for aposta in apostas:
                usuario = User.objects.get(id=aposta.usuario.id)
                usuario.profile.credito = usuario.profile.credito + partida.premiacao
                usuario.profile.apostou = False
                usuario.save()
        elif(apostas.count() > 1):
            premio = partida.premiacao
            premio = premio / apostas.count()
            for aposta in apostas:
                usuario = User.objects.get(id=aposta.usuario.id)
                usuario.profile.credito = usuario.profile.credito + premio
                usuario.profile.apostou = False
                usuario.save()
        else:
            apostas = Apostas.objects.filter(partida=instance.partida.id)
            for aposta in apostas:
                usuario = User.objects.get(id=aposta.usuario.id)
                usuario.profile.credito = usuario.profile.credito + aposta.valor_aposta
                usuario.profile.apostou = False
                usuario.save()
    partida.premiacaoDistribuida = True
    partida.save()
    rodada.permitirApostas = False
    rodada.save()
    usuarios = User.objects.all()
    for usuario in usuarios:
        usuario.profile.apostou = False
        usuario.save()