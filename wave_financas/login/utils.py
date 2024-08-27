from principal.models import Usuario


# FUNÇÃO QUE REALIZA VALIDAÇÃO DOS USUÁRIOS
def autenticacao(email, senha):
    try:
        usuario = Usuario.objects.get(email=email)

        if senha == usuario.senha:
            usuario_dados = {'usuario_id': usuario.id_usuario}

            return True, usuario_dados
        else:
            return False, 'Credenciais inválidas.'

    except Usuario.DoesNotExist:
        return False, 'Credenciais inválidas.'