from .utils import perfil
from django.db.models import Sum
from .models import Receita, Despesa
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import render, redirect


# FUNÇÃO DE CONTROLE PERFIL DO USUÁRIO E LAYOUT PRINCIPAL
def home(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            total_receitas = Receita.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(Sum('valor'))['valor__sum'] or 0
            total_despesas = Despesa.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(Sum('valor'))['valor__sum'] or 0
            saldo = total_receitas - total_despesas

            contexto['total_receitas'] = total_receitas
            contexto['total_despesas'] = total_despesas
            contexto['saldo'] = saldo

            hoje = datetime.today()
            primeiro_dia = (hoje.replace(day=1) - timedelta(days=1)).replace(day=1)
            ultimo_dia = hoje.replace(day=1) - timedelta(days=1)

            entradas_mes = Receita.objects.filter(id_usuario=usuario_id, status='efetuada', data_receita__range=[
                primeiro_dia, ultimo_dia]).values('data_receita').annotate(total=Sum('valor')).order_by('data_receita')
            entradas_formatadas = [
                {'data': entrada['data_receita'].strftime('%Y-%m-%d'), 'total': float(entrada['total'])}
                for entrada in entradas_mes
            ]

            contexto['entradas_mes'] = entradas_formatadas

            return render(request, 'principal/home.html', contexto)
        else:
            return redirect('login')


# FUNÇÃO QUE RETORNAR OS DADOS FILTRADOS PARA ATUALIZAR GRÁFICO DE ÁREA
def filtrar_lancamentos(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            tipo_lancamento = request.GET.get('tipo-lancamento')
            periodo_inicial = request.GET.get('periodo-inicial')
            periodo_final = request.GET.get('periodo-final')

            if tipo_lancamento == 'entrada':
                dados_filtrados = Receita.objects.filter(
                    id_usuario=usuario_id,
                    status='efetuada',
                    data_receita__range=[periodo_inicial, periodo_final]
                ).values('data_receita').annotate(total=Sum('valor')).order_by('data_receita')

                dados_formatados = [
                    {'data': entrada['data_receita'].strftime('%Y-%m-%d'), 'total': float(entrada['total'])}
                    for entrada in dados_filtrados
                ]

            elif tipo_lancamento == 'saida':
                dados_filtrados = Despesa.objects.filter(
                    id_usuario=usuario_id,
                    status='efetuada',
                    data_despesa__range=[periodo_inicial, periodo_final]
                ).values('data_despesa').annotate(total=Sum('valor')).order_by('data_despesa')

                dados_formatados = [
                    {'data': entrada['data_despesa'].strftime('%Y-%m-%d'), 'total': float(entrada['total'])}
                    for entrada in dados_filtrados
                ]

            return JsonResponse(dados_formatados, safe=False)