from .forms import MetasForm
from principal.utils import perfil
from principal.models import Metas, Usuario
from django.shortcuts import render, redirect



# FUNÇÃO CADASTRA E EXIBE AS METAS
def metas(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == "GET":
        if usuario_id:
            contexto = perfil(request)
            metas = Metas.objects.filter(id_usuario=usuario_id)
            contexto['metas'] = metas

            return render(request, 'sistema/metas.html', contexto)
        else:
            return redirect('login')

    elif request.method == "POST":
        form = MetasForm(request.POST)

        if form.is_valid():
            usuario_instance = Usuario.objects.get(id_usuario=usuario_id)
            nova_meta = form.save(commit=False)
            nova_meta.id_usuario = usuario_instance

            nova_meta.save()
            return redirect('metas')