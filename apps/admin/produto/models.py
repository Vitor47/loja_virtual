from django.contrib.auth.models import User
from django.db import models


class ProdutoCategoria(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    nome = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)
    icone = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "administrador_produto_categoria"

    def __str__(self):
        return self.nome


class ProdutoAtributo(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
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

    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    tipo_id = models.IntegerField(choices=TIPO_CHOICES, null=False, blank=False)

    class Meta:
        db_table = "administrador_produto_tipo"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    nome = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    quantidade = models.IntegerField(null=False, blank=False)
    desconto = models.DecimalField(max_digits=12, decimal_places=2, null=True)
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
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    imagem = models.ImageField(upload_to="produto/imagens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    data_cad = models.DateField(null=False)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "administrador_produto_imagens"

    def __str__(self):
        return self.id


class ProdutoAtributoProduto(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    atributo = models.ForeignKey(ProdutoAtributo, on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "administrador_produto_atributo_produto"

    def __str__(self):
        return self.id


class ProdutoDiamentro(models.Model):
    CODIGO_SERVICO_CHOICES = (
        ("04014", "SEDEX à vista"),
        ("04065", "SEDEX à vista pagamento na entrega"),
        ("04510", "PAC à vista"),
        ("04707", "PAC à vista pagamento na entrega"),
        ("40169", "SEDEX 12 ( à vista e a faturar)"),
        ("40215", "SEDEX 10 (à vista e a faturar)"),
        ("40290", "SEDEX Hoje Varejo"),
    )

    FORMATO_CHOICES = (
        (1, "Formato caixa/pacote"),
        (2, "Formato rolo/prisma"),
        (3, "Envelope"),
    )

    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    nCdServico = models.CharField(
        choices=CODIGO_SERVICO_CHOICES, max_length=200, null=False, blank=False
    )
    sCepOrigem = models.CharField(max_length=200, null=False, blank=False)
    sCepDestino = models.CharField(max_length=200, null=True, blank=False)
    nVlPeso = models.CharField(max_length=200, null=False, blank=False)
    nCdFormato = models.IntegerField(choices=FORMATO_CHOICES, null=False, blank=False)
    nVlComprimento = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    nVlAltura = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    nVlLargura = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    nVlDiametro = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    class Meta:
        db_table = "administrador_produto_diametro"

    def __str__(self):
        return self.id


class ProdutoDiamentroProduto(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    diametro = models.ForeignKey(ProdutoDiamentro, on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "administrador_produto_diametro_produto"

    def __str__(self):
        return self.id
