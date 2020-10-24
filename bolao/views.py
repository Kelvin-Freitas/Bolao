from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Partida, Apostas, Rodada

# Create your views here.
@login_required
def dashboard(request):
    partidas = Partida.objects.filter(partidaRealizada=False)
    try:
        rodada = Rodada.objects.get(permitirApostas=True)
    except Rodada.DoesNotExist:
        rodada = "Sem partidas para apostar por enquanto!"
    return render(request, 'bolao/dashboard.html', {'partidas': partidas, 'rodada': rodada})

@login_required
def aposta(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    return render(request, 'bolao/aposta.html', {'partida': partida})

@login_required
def ranking(request):
    users =  User.objects.order_by('-profile__credito')
    return render(request, 'bolao/ranking.html', {'users': users})

@login_required
def apostar(request):
    data = {}
    if(request.method == 'POST'):
        data['placar-casa'] = request.POST.get('placar-casa')
        data['placar-visitante'] = request.POST.get('placar-visitante')
        data['time-casa'] = request.POST.get('time-casa')
        data['time-visitante'] = request.POST.get('time-visitante')
        data['partidaID'] = request.POST.get('partidaID')
        if(data['placar-casa'] > data['placar-visitante']):
            data['time-vencedor'] = data['time-casa']
        elif(data['placar-visitante'] > data['placar-casa']):
            data['time-vencedor'] = data['time-visitante']
        else:
            data['time-vencedor'] = "EMPATE"
        partida = Partida.objects.get(id=data['partidaID'])
        aposta = Apostas()
        aposta.usuario = request.user
        aposta.aposta_placar_casa = data['placar-casa']
        aposta.aposta_placar_vistante = data['placar-visitante']
        aposta.aposta_vencedor = data['time-vencedor']
        aposta.partida = partida
        aposta.save()
        aposta.atualizar(request.user.id)
    return redirect('/')