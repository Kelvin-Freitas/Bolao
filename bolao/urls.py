from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aposta/<int:pk>/', views.aposta, name='aposta'),
    path('apostar', views.apostar, name='apostar'),
]