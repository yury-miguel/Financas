from . import views
from django.urls import path


urlpatterns = [
    path('portifolio/', views.portifolio, name='portifolio'),
    path('extratos/', views.extratos, name='extratos'),
    path('receitas/cadastro/', views.cadastro_receita, name='cadastro_receita'),
    path('receitas/gestao/', views.gestao_receita, name='gestao_receita'),
    path('receitas/analise/', views.analise_receita, name='analise_receita'),
    path('despesas/cadastro/', views.cadastro_despesa, name='cadastro_despesa'),
    path('despesas/gestao/', views.gestao_despesa, name='gestao_despesa'),
    path('despesas/analise/', views.analise_despesa, name='analise_despesa'),
    path('detalhes_receita/<int:receita_id>/', views.detalhes_receita, name='detalhes_receita'),
    path('detalhes_despesa/<int:despesa_id>/', views.detalhes_despesa, name='detalhes_despesa')
]