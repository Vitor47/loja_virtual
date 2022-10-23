from django.contrib.auth.models import User
from django.db import models

class ProdutoCategoria(models.Model):
	id = models.IntegerField(null=False, primary_key=True, auto_created=True),
	nome = models.CharField(max_length=200, null=False, blank=False)
	slug = models.SlugField(max_length=200, null=False, blank=False)
	icone = models.CharField(max_length=200, null=False, blank=False)

	class Meta:
		db_table = "administrador_produto_categoria"

	def __str__(self):
		return self.nome

class ProdutoAtributo(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    nome = models.CharField(max_length=200, null=False, blank=False)
    valor = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "administrador_produto_atributo"

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
        db_table = "administrador_produto_tipo"

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
    tipo = models.ForeignKey(ProdutoTipo, on_delete=models.CASCADE, null=True)
    data_cad = models.DateField(null=False)
    dat_edit = models.DateField(null=True)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
 
    class Meta:
        db_table = "administrador_produto"

    def __str__(self):
        return self.nome

class ProdutoImagens(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    imagem = models.ImageField(upload_to="produto/imagens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    data_cad = models.DateField(null=False)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "administrador_produto_imagens"

    def __str__(self):
        return self.id

class ProdutoAtributoProduto(models.Model):
	id = models.IntegerField(null=False, primary_key=True, auto_created=True),
	atributo = models.ForeignKey(ProdutoAtributo, on_delete=models.CASCADE, null=True)
	produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)

	class Meta:
		db_table = "administrador_produto_atributo_produto"

	def __str__(self):
		return self.id
