import datetime
from django.db.models import Sum
from principal.utils import perfil
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from principal.models import Receita, Despesa, Categoria, Portifolio, Usuario
from .utils import categoria_receita, categoria_despesa, todas_receitas, todas_despesas



# CADASTRA NOVAS RECEITAS E RENDERIZA O LAYOUT DE CADASTRO
def cadastro_receita(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            categorias = categoria_receita(Categoria, usuario_id)
            contexto['categorias'] = categorias
            return render(request, 'financeiro/cadastro_receita.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_receita = request.POST.get('data_receita')
        efetuada = request.POST.get('efetuada')
        categoria = request.POST.get('categoria')
        nova_categoria = request.POST.get('new-category-name')

        if usuario_id:
            usuario_instancia = Usuario.objects.get(id_usuario=usuario_id)

            if nova_categoria:
                nova_categoria_obj = Categoria(
                    id_usuario=usuario_instancia,
                    descricao=nova_categoria,
                    tipo='receita'
                )
                nova_categoria_obj.save()
                print(nova_categoria)

            elif descricao and valor and data_receita and categoria:
                receita_obj = Receita(
                    id_usuario=usuario_instancia,
                    descricao=descricao,
                    valor=valor,
                    data_receita=data_receita,
                    status=efetuada,
                    categoria=categoria
                )
                receita_obj.save()

        return redirect('cadastro_receita')


# PERMITE LER, DELETAR, ATUALIZAR AS RECEITAS CADASTRADAS
def gestao_receita(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            receitas = todas_receitas(Receita, usuario_id)
            contexto['receitas'] = receitas
            return render(request, 'financeiro/gestao_receita.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "editar":
            receita_id = request.POST.get('receita_id')
            receita = get_object_or_404(Receita, pk=receita_id)

            receita.descricao = request.POST.get('descricao')
            receita.valor = request.POST.get('valor')
            receita.data_receita = request.POST.get('data_receita')
            receita.efetuada = request.POST.get('efetuada') == 'True'
            receita.categoria = request.POST.get('categoria')

            receita.save()
            return redirect('gestao_receita')

        elif acao == 'deletar':
            receita_id = request.POST.get('receita_id')
            receita = get_object_or_404(Receita, pk=receita_id)

            receita.delete()
            return redirect('gestao_receita')


# RETORNA O DADO DESEJADO PARA A EDIÇÃO RECEITAS
def detalhes_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    dados_receita = {
        'id': receita.receita_id,
        'descricao': receita.descricao,
        'valor': receita.valor,
        'efetuada': receita.efetuada,
        'data_receita': receita.data_receita.strftime('%Y-%m-%d'),
        'categoria': receita.categoria,
    }

    return JsonResponse(dados_receita)


# EXIBE ANÁLISES GERAIS DE TODAS AS RECEITAS
def analise_receita(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            total_receitas = Receita.objects.filter(id_usuario=usuario_id).aggregate(Sum('valor'))['valor__sum'] or 0
            receitas_por_categorias = Receita.objects.filter(id_usuario=usuario_id).values('categoria').annotate(
                Sum('valor'))
            dados_formatados = [{'categoria': item['categoria'], 'valor__sum': float(item['valor__sum'])} for item in
                                receitas_por_categorias]


            contexto['total_receitas'] = total_receitas
            contexto['receitas_por_categoria'] = dados_formatados

            return render(request, 'financeiro/analise_receita.html', contexto)
        else:
            return redirect('login')


# CADASTRA NOVAS DESPESAS E RENDERIZA O LAYOUT DE CADASTRO
def cadastro_despesa(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            categorias = categoria_despesa(Categoria, usuario_id)
            contexto['categorias'] = categorias
            return render(request, 'financeiro/cadastro_despesa.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        data_despesa = request.POST.get('data_despesa')
        efetuada = request.POST.get('efetuada')
        categoria = request.POST.get('categoria')
        nova_categoria = request.POST.get('new-category-name')

        if usuario_id:
            usuario_instancia = Usuario.objects.get(id_usuario=usuario_id)

            if nova_categoria:
                nova_categoria_obj = Categoria(
                    id_usuario=usuario_instancia,
                    descricao=nova_categoria,
                    tipo='despesa'
                )
                nova_categoria_obj.save()

            elif descricao and valor and data_despesa and categoria:
                despesa_obj = Despesa(
                    id_usuario=usuario_instancia,
                    descricao=descricao,
                    valor=valor,
                    data_despesa=data_despesa,
                    status=efetuada,
                    categoria=categoria
                )
                despesa_obj.save()

        return redirect('cadastro_despesa')


# PERMITE LER, DELETAR, ATUALIZAR AS DESPESAS CADASTRADAS
def gestao_despesa(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            despesas = todas_receitas(Despesa, usuario_id)
            contexto['despesas'] = despesas
            return render(request, 'financeiro/gestao_despesa.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "editar":
            despesa_id = request.POST.get('despesa_id')
            despesa = get_object_or_404(Despesa, pk=despesa_id)

            despesa.descricao = request.POST.get('descricao')
            despesa.valor = request.POST.get('valor')
            despesa.data_receita = request.POST.get('data_despesa')
            despesa.efetuada = request.POST.get('efetuada') == 'True'
            despesa.categoria = request.POST.get('categoria')

            despesa.save()
            return redirect('gestao_despesa')

        elif acao == 'deletar':
            despesa_id = request.POST.get('despesa_id')
            despesa = get_object_or_404(Despesa, pk=despesa_id)

            despesa.delete()
            return redirect('gestao_despesa')


# RETORNA O DADO DESEJADO PARA A EDIÇÃO DESPESAS
def detalhes_despesa(request, despesa_id):
    despesa = get_object_or_404(Despesa, pk=despesa_id)

    dados_despesa = {
        'id': despesa.despesa_id,
        'descricao': despesa.descricao,
        'valor': despesa.valor,
        'efetuada': despesa.efetuada,
        'data_despesa': despesa.data_despesa.strftime('%Y-%m-%d'),
        'categoria': despesa.categoria,
    }

    return JsonResponse(dados_despesa)


# EXIBE ANÁLISES GERAIS DE TODAS AS DESPESAS
def analise_despesa(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            total_despesas = Despesa.objects.filter(id_usuario=usuario_id).aggregate(Sum('valor'))['valor__sum'] or 0
            despesas_por_categorias = Despesa.objects.filter(id_usuario=usuario_id).values('categoria').annotate(
                Sum('valor'))
            dados_formatados = [{'categoria': item['categoria'], 'valor__sum': float(item['valor__sum'])} for item in
                                despesas_por_categorias]


            contexto['total_despesas'] = total_despesas
            contexto['despesas_por_categoria'] = dados_formatados

            return render(request, 'financeiro/analise_despesa.html', contexto)
        else:
            return redirect('login')


# FUNÇÃO QUE EXIBE TABELA DE EXTRATOS (TRANSAÇÕES) DE DESPESAS E RECEITAS
def extratos(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)

            data_inicio = request.GET.get('data_inicio')
            data_fim = request.GET.get('data_fim')

            extratos_receitas = Receita.objects.filter(id_usuario=usuario_id)
            extratos_despesas = Despesa.objects.filter(id_usuario=usuario_id)

            if data_inicio and data_fim:
                data_inicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d').date()
                data_fim = datetime.datetime.strptime(data_fim, '%Y-%m-%d').date()
                extratos_receitas = extratos_receitas.filter(data_receita__range=(data_inicio, data_fim))
                extratos_despesas = extratos_despesas.filter(data_despesa__range=(data_inicio, data_fim))

            contexto['extratos_receitas'] = extratos_receitas
            contexto['extratos_despesas'] = extratos_despesas

            return render(request, 'financeiro/extratos.html', contexto)
        else:
            return redirect('login')



# FUNÇÃO CADASTRA, EXIBE TODOS PORTIFOLIOS
def portifolio(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            portifolios = Portifolio.objects.filter(id_usuario=usuario_id)
            contexto['portifolios'] = portifolios

            return render(request, 'financeiro/portifolio.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        usuario_instancia = Usuario.objects.get(id_usuario=usuario_id)

        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipo')
        valor_gasto = request.POST.get('valor_gasto')
        valor_retorno = request.POST.get('valor_retorno')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        receita_liquida = float(valor_retorno) - float(valor_gasto)

        portifolio_data = {
            'id_usuario': usuario_instancia,
            'titulo': titulo,
            'descricao': descricao,
            'tipo': tipo,
            'valor_gasto': valor_gasto,
            'valor_retorno': valor_retorno,
            'data_inicio': data_inicio if data_inicio else None,
            'data_fim': data_fim if data_fim else None,
        }

        portifolio_data = {key: value for key, value in portifolio_data.items() if value is not None}

        portifolio = Portifolio(**portifolio_data)
        portifolio.save()

        categoria_portifolio = Categoria(
            id_usuario=usuario_instancia,
            descricao=f"portifolio: {titulo}",
            tipo='receita'
        )
        categoria_portifolio.save()

        receita_portifolio = Receita(
            id_usuario=usuario_instancia,
            descricao=f"Portifolio: {tipo}",
            categoria=categoria_portifolio.descricao,
            valor=receita_liquida,
            data_receita=data_fim if data_fim else data_inicio,
            status='efetuada'
        )
        receita_portifolio.save()

        return redirect('portifolio')