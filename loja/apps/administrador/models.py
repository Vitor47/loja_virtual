from django.contrib.auth.models import User
from django.db import models


class Auditoria(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    user = models.CharField(max_length=200, null=False, blank=False)
    mensagem = models.CharField(max_length=200, null=False, blank=False)
    ip = models.CharField(max_length=200, null=False, blank=False)
    data = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    class Meta:
        db_table = "auditoria"

    def __str__(self):
        return self.id

class Banner(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    status = models.BooleanField(null=False)
    imagem = models.ImageField(upload_to="banner")
    data_cad = models.DateField(null=False)
    dat_edit = models.DateField(null=True)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
 
    class Meta:
        db_table = "banner"

    def __str__(self):
        return self.id
    

class ProdutoCategoria(models.Model):
    CATEGORIA_CHOICES = (
        (1, "Ferramentas"),
        (2, "Tomadas e Interruptores"),
        (3, "Lâmpadas e Luminárias"),
        (4, "Linha de Proteção"),
        (5, "Fios e Cabos"),
        (6, "Diversos"),
    )

    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    categoria_id = models.IntegerField(choices=CATEGORIA_CHOICES, null=False, blank=False)

    class Meta:
        db_table = "produto_categoria"

    def __str__(self):
        return self.nome

class ProdutoAtributo(models.Model):
    ATRIBUTO_CHOICES = (
        (1, "Externa e Interna"),
        (2, "Cor"),
        (3, "Bitola"),
        (4, "Amperagem"),
    )

    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    atributo_id = models.IntegerField(choices=ATRIBUTO_CHOICES, null=False, blank=False)

    class Meta:
        db_table = "produto_atributo"

    def __str__(self):
        return self.nome

class ProdutoTipo(models.Model):
    TIPO_CHOICES = (
        (1, "Ofertas"),
        (2, "Novidades"),
        (3, "Todos"),
    )

    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    tipo_id = models.IntegerField(choices=TIPO_CHOICES, null=False, blank=False)

    class Meta:
        db_table = "produto_tipo"

    def __str__(self):
        return self.nome

class Produto(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    nome = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)
    valor = models.DecimalField(max_digits = 12, decimal_places = 2)
    quantidade = models.IntegerField(null=False, blank=False)
    desconto = models.DecimalField(max_digits = 12, decimal_places = 2, null=True)
    imagem_principal = models.ImageField(upload_to="produto")
    descricao = models.TextField(null=True)
    status = models.BooleanField(null=False)
    categoria = models.ForeignKey(ProdutoCategoria, on_delete=models.CASCADE, null=True)
    atributo = models.ForeignKey(ProdutoAtributo, on_delete=models.CASCADE, null=True)
    tipo = models.ForeignKey(ProdutoTipo, on_delete=models.CASCADE, null=True)
    data_cad = models.DateField(null=False)
    dat_edit = models.DateField(null=True)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
 
    class Meta:
        db_table = "produto"

    def __str__(self):
        return self.nome

class ProdutoImagens(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    imagem = models.ImageField(upload_to="produto/imagens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    data_cad = models.DateField(null=False)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "produto_imagens"

    def __str__(self):
        return self.id

class Configuracao(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    nome = models.CharField(max_length=200, null=False, blank=False)
    valor = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "configuracao"

    def __str__(self):
        return self.id

class Cliente(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    nome = models.CharField(max_length=200, null=False, blank=False)
    user = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    telefone = models.CharField(max_length=200, null=False, blank=False)
    cpf_cnpj = models.CharField(max_length=200, null=False, blank=False)
    data_nascimento = models.DateField(null=False)
    senha = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "cliente"

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    cep = models.CharField(max_length=200, null=False, blank=False)
    estado = models.CharField(max_length=200, null=False, blank=False)
    cidade = models.CharField(max_length=200, null=False, blank=False)
    bairro = models.CharField(max_length=200, null=True, blank=False)
    logradouro = models.CharField(max_length=200, null=True, blank=False)
    nr_casa = models.IntegerField(null=True, blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = "cliente_endereco"
    
    def __str__(self):
        return self.id