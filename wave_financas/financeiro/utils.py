# FUNÇÃO RESPONSÁVEL POR MOSTRAR OS DADOS CATEGÓRICOS DE RECEITA DO USUÁRIO
def categoria_receita(classe, usuario):
    categorias_receitas = classe.objects.filter(id_usuario=usuario, tipo='receita')
    return categorias_receitas


# FUNÇÃO RESPONSÁVEL POR MOSTRAR OS DADOS CATEGÓRICOS DE DESPESAS DO USUÁRIO
def categoria_despesa(classe, usuario):
    categorias_despesas = classe.objects.filter(id_usuario=usuario, tipo='despesa')

    return categorias_despesas


# FUNÇÃO QUE RECUPERA TODAS RECEITAS CADASTRADAS PELO USUÁRIO
def todas_receitas(classe, usuario):
    receitas = classe.objects.filter(id_usuario=usuario)

    return receitas


# FUNÇÃO QUE RECUPERA TODAS DESPESAS CADASTRADAS PELO USUÁRIO
def todas_despesas(classe, usuario):
    despesas = classe.objects.filter(id_usuario=usuario)

    return despesas