from . import views
from django.urls import path


urlpatterns = [
    path('relatorio/gastos/', views.gastos, name='gastos'),
    path('relatorio/operacoes/', views.contas, name='contas'),
    path('relatorio/balanco/', views.balanco, name='balanco'),
]