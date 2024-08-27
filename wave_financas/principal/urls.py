from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('filtrar-lancamentos', views.filtrar_lancamentos, name='filtrar_lancamentos'),
]
