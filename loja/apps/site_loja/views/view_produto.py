from django.shortcuts import render, redirect
from django.db.models import Q
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from loja.apps.apps_administrador.produto.models import Produto, ProdutoCategoria, ProdutoTipo, ProdutoImagens
from ..utils import Correios

def produtos(request):
    if request.method == "GET":
        list_products = Produto.objects.filter(status=True).exclude(quantidade=0).order_by('-id')
        list_categorys = ProdutoCategoria.objects.all().order_by('-id')
        
        consulta_nome = request.GET.get('produtos_name')
        if consulta_nome is not None:
            list_products = list_products.filter(nome__icontains=consulta_nome, status=True).exclude(quantidade=0).order_by('-id')

        categoria_slug = request.GET.getlist('categoria_slug[]', None)
        if len(categoria_slug) > 0:
            products = []
            categorys = []

            for categoria in list_categorys:
                for y in categoria_slug:
                    if categoria.slug == y:
                        marcado = True
                        break
                    else:
                        marcado = False

                categoria = {
                    'id': categoria.id,
                    'nome': categoria.nome,
                    'slug': categoria.slug,
                    'marcado': marcado
                }
                categorys.append(categoria)

            for item_category in categoria_slug:
                categoria = ProdutoCategoria.objects.get(slug=item_category)

                list_products = Produto.objects.filter(categoria_id=categoria.id, status=True).exclude(quantidade=0).order_by('-id')
                for produto in list_products:
                    if produto.desconto is not None and produto.desconto != "":
                        valor_com_desconto = produto.valor - produto.desconto
                        percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto.valor))
                    else:
                        valor_com_desconto = None
                        percent_descont = None

                    produto = {
                        'id': produto.id,
                        'nome': produto.nome,
                        'imagem_principal': produto.imagem_principal,
                        'valor_inicial': produto.valor,
                        'valor_com_desconto': valor_com_desconto,
                        'percent_desconto': percent_descont,
                        'slug': produto.slug
                    }
                    products.append(produto)

            default_page = 1
            page = request.GET.get('page', default_page)
            # Paginate items
            items_per_page = 10
            paginator = Paginator(products, items_per_page)

            try:
                items_page = paginator.page(page)
            except PageNotAnInteger:
                items_page = paginator.page(default_page)
            except EmptyPage:
                items_page = paginator.page(paginator.num_pages)

            context = {}
            context['tamanho_array_products'] = len(products)
            context['produtos'] = items_page
            context['categorias'] = categorys
            return TemplateResponse(request, "produtos/index.html", context)

        valor_checkbox = request.GET.get('valor')
        if valor_checkbox is not None:
            products_filter_money = []
            valor = ""
            if valor_checkbox == "maior_100":
                valor = "maior_100"
                for produto in list_products:
                    if produto.valor >= 100.00:
                        if produto.desconto is not None and produto.desconto != "":
                            valor_com_desconto = produto.valor - produto.desconto
                            percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto.valor))
                        else:
                            valor_com_desconto = None
                            percent_descont = None

                        produto = {
                            'id': produto.id,
                            'nome': produto.nome,
                            'imagem_principal': produto.imagem_principal,
                            'valor_inicial': produto.valor,
                            'valor_com_desconto': valor_com_desconto,
                            'percent_desconto': percent_descont,
                            'slug': produto.slug
                        }
                        products_filter_money.append(produto)
            elif valor_checkbox == "menor_100":
                valor = "menor_100"
                for produto in list_products:
                    if produto.valor < 100.00:
                        for produto in list_products:
                            if produto.desconto is not None and produto.desconto != "":
                                valor_com_desconto = produto.valor - produto.desconto
                                percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto.valor))
                            else:
                                valor_com_desconto = None
                                percent_descont = None

                            produto = {
                                'id': produto.id,
                                'nome': produto.nome,
                                'imagem_principal': produto.imagem_principal,
                                'valor_inicial': produto.valor,
                                'valor_com_desconto': valor_com_desconto,
                                'percent_desconto': percent_descont,
                                'slug': produto.slug
                            }
                            products_filter_money.append(produto)

            default_page = 1
            page = request.GET.get('page', default_page)
            # Paginate items
            items_per_page = 10
            paginator = Paginator(products_filter_money, items_per_page)

            try:
                items_page = paginator.page(page)
            except PageNotAnInteger:
                items_page = paginator.page(default_page)
            except EmptyPage:
                items_page = paginator.page(paginator.num_pages)

            context = {}
            context['tamanho_array_products'] = len(products_filter_money)
            context['produtos'] = items_page
            context['valor'] = valor
            context['categorias'] = list_categorys
            return TemplateResponse(request, "produtos/index.html", context)

        products = []
        for produto in list_products:
            if produto.desconto is not None and produto.desconto != "":
                valor_com_desconto = produto.valor - produto.desconto
                percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto.valor))
            else:
                valor_com_desconto = None
                percent_descont = None

            produto = {
                'id': produto.id,
                'nome': produto.nome,
                'imagem_principal': produto.imagem_principal,
                'valor_inicial': produto.valor,
                'valor_com_desconto': valor_com_desconto,
                'percent_desconto': percent_descont,
                'slug': produto.slug
            }
            products.append(produto)

        default_page = 1
        page = request.GET.get('page', default_page)
        items_per_page = 10
        paginator = Paginator(products, items_per_page)

        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)
        return render(request, "produtos/index.html", {'produtos': items_page, 'categorias': list_categorys, 'tamanho_array_products': len(list_products)})


def categoria_produto(request, slug):
    if request.method == "GET":
        list_categorys = ProdutoCategoria.objects.all().order_by('-id')
        category = ProdutoCategoria.objects.get(slug=slug)
        list_products = Produto.objects.filter(status=True, categoria_id=category.id).exclude(quantidade=0).order_by('-id')

        default_page = 1
        page = request.GET.get('page', default_page)
        items_per_page = 10
        paginator = Paginator(list_products, items_per_page)

        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)
        return render(request, "produtos/index.html", {'produtos': items_page, 'categorias': list_categorys})

def detalhes_produto(request, slug):
    if request.method == "GET":
        produto = Produto.objects.get(status=True, slug=slug)
        categoria_produto = ProdutoCategoria.objects.get(
            Q(id=produto.categoria_id)
        )

        tipo_produto = ProdutoTipo.objects.get(
            Q(id=produto.tipo_id)
        )

        imagens_produto = ProdutoImagens.objects.filter(
            Q(produto_id=produto.id)
        )

        produtos_relacionados = Produto.objects.filter(
            Q(categoria_id=produto.categoria_id) and
            Q(tipo_id=produto.tipo_id)
        ).exclude(quantidade=0).order_by('-id')[:10]

        products_relacioned = []
        for produto_relacionado in produtos_relacionados:
            if produto_relacionado.desconto is not None and produto_relacionado.desconto != "":
                valor_com_desconto = produto_relacionado.valor - produto_relacionado.desconto
                percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto_relacionado.valor))
            else:
                valor_com_desconto = None
                percent_descont = None

            produto_relacionado = {
                'id': produto_relacionado.id,
                'nome': produto_relacionado.nome,
                'imagem_principal': produto_relacionado.imagem_principal,
                'valor_inicial': produto_relacionado.valor,
                'valor_com_desconto': valor_com_desconto,
                'percent_desconto': percent_descont,
                'slug': produto_relacionado.slug
            }
            products_relacioned.append(produto_relacionado)

        if produto.desconto is not None and produto.desconto != "":
            valor_com_desconto = produto.valor - produto.desconto
            percent_descont = 100 - ((float(valor_com_desconto) * 100) // float(produto.valor))
        else:
            valor_com_desconto = None
            percent_descont = None

        produto = {
            'id': produto.id,
            'nome': produto.nome,
            'imagem_principal': produto.imagem_principal,
            'valor_inicial': produto.valor,
            'valor_com_desconto': valor_com_desconto,
            'percent_desconto': percent_descont,
            'descricao': produto.descricao,
            'slug': produto.slug,
            'categoria': produto.categoria_id,
            'tipo': produto.tipo_id
        }

        context = {}
        context['produto'] = produto
        context['produto_categoria'] = categoria_produto
        context['produto_tipo'] = tipo_produto
        context['imagens_produto'] = imagens_produto
        context['tamanho_array_produtos_relacionados'] = len(products_relacioned)
        context['produtos_relacionados'] = products_relacioned
        return TemplateResponse(request, "produtos/detalhes/index.html", context)
    elif request.method == "POST":
        class DadosEncomenda():
            cod = 0
            cep_envia = 0
            cep_recebe = 0
            peso = 0.0
            formato = 0
            comprimento = 0
            altura = 0
            largura = 0
            diametro = 0

            def __init__(self):
                self.cod = '40010'
                self.cep_envia = '97400000'
                self.cep_recebe = '97200000'
                self.peso = '1'
                self.formato = '1'
                self.comprimento = '20'
                self.altura = '5'
                self.largura = '15'
                self.diametro = '0'

        correio = Correios()
        dados_encomenda = DadosEncomenda()

        tags_name, retorno_envio = correio.frete(
            dados_encomenda.cod, dados_encomenda.cep_envia, dados_encomenda.cep_recebe, dados_encomenda.peso, dados_encomenda.formato,
            dados_encomenda.comprimento, dados_encomenda.altura, dados_encomenda.largura, dados_encomenda.diametro, mao_propria='N',
            valor_declarado='0', aviso_recebimento='N',
            empresa='', senha='', toback='xml'
        )

        calculo_frete = correio._getDados(tags_name, retorno_envio)
        return JsonResponse({'context': calculo_frete}, status=200)