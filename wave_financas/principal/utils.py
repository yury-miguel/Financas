import base64
from .models import Usuario


# FUNÇÃO ULTILIZADA PARA MANTER O PERFIL DO USUÁRIO
def perfil(request):
    usuario_id = request.session.get('usuario_id')

    if usuario_id:
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
            nome = usuario.nome
            email = usuario.email
            telefone = usuario.telefone
            foto = codifica_base64(usuario.foto)

            contexto = {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'foto_base64': foto
            }
            return contexto

        except Usuario.DoesNotExist:
            return {}
    else:
        return {}


# FUNÇÃO QUE FAZ O TRATAMENTO PARA RENDERIZAR IMAGEM DO USUARIO NO FRONTEND
def codifica_base64(foto_binaria):
    nova_foto = base64.b64encode(foto_binaria).decode('utf-8')
    return nova_foto