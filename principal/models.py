from django.db import models

# Create your models here.

SELECOES = [
    ("BRA", "Brasil"),
    ("ARG", "Argentina"),
    ("RUS", "Rússia"),
    ("NGA", "Nigéria"),
    ("SEN", "Senegal"),
    ("GBR", "Reino Unido"),
]

class Partida(models.Model):
    selecao_um = models.CharField(max_length=40, choices=SELECOES)
    selecao_dois = models.CharField(max_length=40, choices=SELECOES)
    gols_selecao_um = models.PositiveSmallIntegerField()
    gols_selecao_dois = models.PositiveSmallIntegerField()
    resultado_partida = models.CharField(max_length=40, choices=SELECOES)

    def __str__(self):
        return '%s x %s' % (self.selecao_um, self.selecao_dois)
    
