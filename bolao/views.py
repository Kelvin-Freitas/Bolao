from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Partida

# Create your views here.
@login_required
def dashboard(request):
    partidas = Partida.objects.filter(partidaRealizada=False)
    return render(request, 'bolao/dashboard.html', {'partidas': partidas})

@login_required
def aposta(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    return render(request, 'bolao/aposta.html', {'partida': partida})