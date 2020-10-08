from django.shortcuts import render

# Create your views here.
def partidas_list(request):
    return render(request, 'bolao/partidas_list.html', {})