from . import views
from django.urls import path

urlpatterns = [
    path('painel/performance/', views.performance, name='performance'),
    path('painel/operacoes/', views.operacoes, name='operacoes'),
    path('painel/giro/', views.giro, name='giro'),
]