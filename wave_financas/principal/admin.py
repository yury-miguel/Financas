from django.contrib import admin
from .models import Usuario, Categoria, Receita, Despesa, Metas, Portifolio

# REGISTRANDO OS MODELOS CASO SEJA NECESSÁRIO GERENCIAR OS DADOS
# ATRAVÉS DO PAINEL ADMINISTRATIVO DJANGO

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Receita)
admin.site.register(Despesa)
admin.site.register(Metas)
admin.site.register(Portifolio)