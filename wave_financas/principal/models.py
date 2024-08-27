from django.db import models

# MODELOS CORRESPONDENTES AS TABELAS CRIADAS NO POSTGRESQL
# DISPONÍVEIS EM /Banco/banco.sql

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    telefone = models.CharField(max_length=15)
    senha = models.CharField(max_length=255)
    foto = models.BinaryField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuario'

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    id_categoria = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'categoria'

class Receita(models.Model):
    id_receita = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_receita = models.DateField()
    status = models.CharField(max_length=50)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'receita'

class Despesa(models.Model):
    id_despesa = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_despesa = models.DateField()
    status = models.CharField(max_length=50)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    
    class Meta:
        managed = False
        db_table = 'despesa'

class Metas(models.Model):
    id_meta = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    data_meta = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'metas'

class Portifolio(models.Model):
    id_portifolio = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=700)
    tipo = models.CharField(max_length=20)
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2)
    valor_retorno = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'portifolio'