from datetime import date
from django.db.models import Sum
from principal.utils import perfil
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from principal.models import Receita, Despesa, Portifolio

# DICIONÁRIO DOS MESES EM PORTUGUÊS
meses_portugues = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}


def get_periodic_data(queryset, field, start_date, end_date):
    return queryset.filter(**{
        f"{field}__gte": start_date,
        f"{field}__lte": end_date
    }).aggregate(Sum('valor'))['valor__sum'] or 0


# INFORMA OS DADOS DE ACORDO COM OS DASHBOARDS DE PERFORMANCES
def performance(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            hoje = now().date()
            inicio_ano = date(hoje.year, 1, 1)
            inicio_mes = date(hoje.year, hoje.month, 1)
            inicio_trimestre = date(hoje.year, (hoje.month - 1) // 3 * 3 + 1, 1)
            inicio_semestre = inicio_ano if hoje.month <= 6 else date(hoje.year, 7, 1)

            total_receitas = Receita.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(Sum('valor')
                                                                                                     )[
                                 'valor__sum'] or 0
            total_despesas = Despesa.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(Sum('valor')
                                                                                                     )[
                                 'valor__sum'] or 0
            saldo = total_receitas - total_despesas

            receitas_mensal = get_periodic_data(Receita.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                'data_receita', inicio_mes, hoje)
            despesas_mensal = get_periodic_data(Despesa.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                'data_despesa', inicio_mes, hoje)
            saldo_mensal = receitas_mensal - despesas_mensal

            receitas_trimestral = get_periodic_data(Receita.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                    'data_receita', inicio_trimestre, hoje)
            despesas_trimestral = get_periodic_data(Despesa.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                    'data_despesa', inicio_trimestre, hoje)
            saldo_trimestral = receitas_trimestral - despesas_trimestral

            receitas_semestral = get_periodic_data(Receita.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                   'data_receita', inicio_semestre, hoje)
            despesas_semestral = get_periodic_data(Despesa.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                                   'data_despesa', inicio_semestre, hoje)
            saldo_semestral = receitas_semestral - despesas_semestral

            receitas_anual = get_periodic_data(Receita.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                               'data_receita', inicio_ano, hoje)
            despesas_anual = get_periodic_data(Despesa.objects.filter(id_usuario=usuario_id, status='efetuada'),
                                               'data_despesa', inicio_ano, hoje)
            saldo_anual = receitas_anual - despesas_anual

            portifolio = Portifolio.objects.filter(id_usuario=usuario_id)

            qtd_projetos = portifolio.filter(tipo='Projeto').count()
            ganho_projetos = portifolio.filter(tipo='Projeto').aggregate(Sum('valor_retorno'))[
                                 'valor_retorno__sum'] or 0
            gasto_projetos = portifolio.filter(tipo='Projeto').aggregate(Sum('valor_gasto'))['valor_gasto__sum'] or 0

            qtd_clientes = portifolio.filter(tipo='Cliente').count()
            ganho_clientes = portifolio.filter(tipo='Cliente').aggregate(Sum('valor_retorno'))[
                                 'valor_retorno__sum'] or 0
            gasto_clientes = portifolio.filter(tipo='Cliente').aggregate(Sum('valor_gasto'))['valor_gasto__sum'] or 0

            qtd_ativos = portifolio.filter(tipo='Ativos').count()
            ganho_ativos = portifolio.filter(tipo='Ativos').aggregate(Sum('valor_retorno'))['valor_retorno__sum'] or 0
            gasto_ativos = portifolio.filter(tipo='Ativos').aggregate(Sum('valor_gasto'))['valor_gasto__sum'] or 0

            contexto.update({
                'div': 'performance',
                'total_receitas': total_receitas,
                'total_despesas': total_despesas,
                'saldo': saldo,
                'receitas_mensal': receitas_mensal,
                'despesas_mensal': despesas_mensal,
                'saldo_mensal': saldo_mensal,
                'receitas_trimestral': receitas_trimestral,
                'despesas_trimestral': despesas_trimestral,
                'saldo_trimestral': saldo_trimestral,
                'receitas_semestral': receitas_semestral,
                'despesas_semestral': despesas_semestral,
                'saldo_semestral': saldo_semestral,
                'receitas_anual': receitas_anual,
                'despesas_anual': despesas_anual,
                'saldo_anual': saldo_anual,
                'qtd_projetos': qtd_projetos,
                'ganho_projetos': ganho_projetos,
                'gasto_projetos': gasto_projetos,
                'qtd_clientes': qtd_clientes,
                'ganho_clientes': ganho_clientes,
                'gasto_clientes': gasto_clientes,
                'qtd_ativos': qtd_ativos,
                'ganho_ativos': ganho_ativos,
                'gasto_ativos': gasto_ativos,
            })

            return render(request, 'painel/dash1.html', contexto)
        else:
            return redirect('login')


# INFORMA OS DADOS DE ACORDO COM OS DASHBOARD DE OPERAÇÕES
def operacoes(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            receitas = Receita.objects.filter(id_usuario=usuario_id)
            despesas = Despesa.objects.filter(id_usuario=usuario_id)

            receitas_por_mes = Receita.objects.filter(id_usuario=usuario_id, status='efetuada').annotate(
                month=TruncMonth('data_receita')).values('month').annotate(total=Sum('valor')).order_by('month')

            despesas_por_mes = Despesa.objects.filter(id_usuario=usuario_id, status='efetuada').annotate(
                month=TruncMonth('data_despesa')).values('month').annotate(total=Sum('valor')).order_by('month')

            receitas_data = {data['month'].strftime('%Y-%m'): float(data['total']) for data in receitas_por_mes}
            despesas_data = {data['month'].strftime('%Y-%m'): float(data['total']) for data in despesas_por_mes}
            meses = sorted(set(list(receitas_data.keys()) + list(despesas_data.keys())))

            receitas_chart_data = [receitas_data.get(mes, 0) for mes in meses]
            despesas_chart_data = [despesas_data.get(mes, 0) for mes in meses]

            eficiencia_data = [
                receitas_chart_data[i] / despesas_chart_data[i] if despesas_chart_data[i] != 0 else 0
                for i in range(len(meses))
            ]

            contexto.update({
                'receitas': receitas,
                'despesas': despesas,
                'meses': meses,
                'receitas_chart_data': receitas_chart_data,
                'despesas_chart_data': despesas_chart_data,
                'eficiencia_data': eficiencia_data,
            })

            return render(request, 'painel/dash2.html', contexto)
        else:
            return redirect('login')


# INFORMA OS DADOS DE ACORDO COM OS DASHBOARDS DE GIROS
def giro(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            receitas_por_mes = Receita.objects.filter(id_usuario=usuario_id, status='efetuada').annotate(
                month=TruncMonth('data_receita')).values('month').annotate(total=Sum('valor')).order_by('month')

            despesas_por_mes = Despesa.objects.filter(id_usuario=usuario_id, status='efetuada').annotate(
                month=TruncMonth('data_despesa')).values('month').annotate(total=Sum('valor')).order_by('month')

            receitas_data = {data['month'].strftime('%Y-%m'): float(data['total']) for data in receitas_por_mes}
            despesas_data = {data['month'].strftime('%Y-%m'): float(data['total']) for data in despesas_por_mes}
            meses = sorted(set(list(receitas_data.keys()) + list(despesas_data.keys())))
            meses_nomes = [meses_portugues[int(mes.split('-')[1])] for mes in meses]

            receitas_chart_data = [receitas_data.get(mes, 0) for mes in meses]
            despesas_chart_data = [despesas_data.get(mes, 0) for mes in meses]

            receitas_recebidas = Receita.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(
                total=Sum('valor'))['total'] or 0
            receitas_nao_recebidas = Receita.objects.filter(id_usuario=usuario_id, status='nao_efetuada').aggregate(
                total=Sum('valor'))['total'] or 0
            despesas_pagas = Despesa.objects.filter(id_usuario=usuario_id, status='efetuada').aggregate(
                total=Sum('valor'))['total'] or 0
            despesas_nao_pagas = Despesa.objects.filter(id_usuario=usuario_id, status='nao_efetuada').aggregate(
                total=Sum('valor'))['total'] or 0

            contexto.update({
                'meses': meses_nomes,
                'receitas_chart_data': receitas_chart_data,
                'despesas_chart_data': despesas_chart_data,
                'receitas_recebidas': receitas_recebidas,
                'receitas_nao_recebidas': receitas_nao_recebidas,
                'despesas_pagas': despesas_pagas,
                'despesas_nao_pagas': despesas_nao_pagas,
            })

            return render(request, 'painel/dash3.html', contexto)
        else:
            return redirect('login')