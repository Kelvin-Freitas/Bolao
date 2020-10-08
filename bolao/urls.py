from django.urls import path
from . import views

urlpatterns = [
    path('', views.partidas_list, name='partidas_list'),
]