from .forms import LoginForm
from .utils import autenticacao
from django.contrib import messages
from django.shortcuts import render, redirect


# FUNÇÃO QUE REALIZA VERIFICAÇÃO DE AUTENTICIDADE PARA O LOGIN
def login_view(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            senha = formulario.cleaned_data['senha']
            verificacao, dado_erro = autenticacao(email=email, senha=senha)
            
            if verificacao:
                dados = dado_erro
                request.session['usuario_id'] = dados['usuario_id']
                
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('home')
            else:
                messages.error(request, dado_erro)
        else:
            messages.error(request, 'Erro ao validar o formulário')
    else:
        formulario = LoginForm()

    return render(request, 'login/login.html', {'form': formulario})