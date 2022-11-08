from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

from loja.apps.apps_administrador.produto.models import Produto, ProdutoCategoria

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
                        desconto = produto.desconto / 100
                        percent_descont = produto.valor * desconto
                    else:
                        valor_com_desconto = None
                        percent_descont = None

                    produto = {
                        'id': produto.id,
                        'nome': produto.nome,
                        'imagem_principal': produto.imagem_principal,
                        'valor_inicial': produto.valor,
                        'valor_com_desconto': valor_com_desconto,
                        'percent_desconto': percent_descont
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
            products = []
            valor = ""
            if valor_checkbox == "maior_100":
                valor = "maior_100"
                for produto in list_products:
                    if produto.valor >= 100.00:
                        for produto in list_products:
                            if produto.desconto is not None and produto.desconto != "":
                                valor_com_desconto = produto.valor - produto.desconto
                                desconto = produto.desconto / 100
                                percent_descont = produto.valor * desconto
                            else:
                                valor_com_desconto = None
                                percent_descont = None

                            produto = {
                                'id': produto.id,
                                'nome': produto.nome,
                                'imagem_principal': produto.imagem_principal,
                                'valor_inicial': produto.valor,
                                'valor_com_desconto': valor_com_desconto,
                                'percent_desconto': percent_descont
                            }
                            products.append(produto)
            elif valor_checkbox == "menor_100":
                valor = "menor_100"
                for produto in list_products:
                    if produto.valor < 100.00:
                        for produto in list_products:
                            if produto.desconto is not None and produto.desconto != "":
                                valor_com_desconto = produto.valor - produto.desconto
                                desconto = produto.desconto / 100
                                percent_descont = produto.valor * desconto
                            else:
                                valor_com_desconto = None
                                percent_descont = None

                            produto = {
                                'id': produto.id,
                                'nome': produto.nome,
                                'imagem_principal': produto.imagem_principal,
                                'valor_inicial': produto.valor,
                                'valor_com_desconto': valor_com_desconto,
                                'percent_desconto': percent_descont
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
            context['produtos'] = products
            context['valor'] = valor
            context['categorias'] = list_categorys
            return TemplateResponse(request, "produtos/index.html", context)

        products = []
        for produto in list_products:
            if produto.desconto is not None and produto.desconto != "":
                valor_com_desconto = produto.valor - produto.desconto
                desconto = produto.desconto / 100
                percent_descont = produto.valor * desconto
            else:
                valor_com_desconto = None
                percent_descont = None

            produto = {
                'id': produto.id,
                'nome': produto.nome,
                'imagem_principal': produto.imagem_principal,
                'valor_inicial': produto.valor,
                'valor_com_desconto': valor_com_desconto,
                'percent_desconto': percent_descont
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
        return render(request, "produtos/index.html", {'produtos': items_page, 'categorias': list_categorys, 'tamanho_array_products': len(list_products)})


def categoria_produto(request, slug):
    if request.method == "GET":
        list_categorys = ProdutoCategoria.objects.all().order_by('-id')
        category = ProdutoCategoria.objects.get(slug=slug)
        list_products = Produto.objects.filter(status=True, categoria_id=category.id).exclude(quantidade=0).order_by('-id')

        default_page = 1
        page = request.GET.get('page', default_page)
        # Paginate items
        items_per_page = 10
        paginator = Paginator(list_products, items_per_page)

        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)
        return render(request, "produtos/index.html", {'produtos': items_page, 'categorias': list_categorys})

def detalhes_produto(request):
    if request.method == "GET":
        return render(request, "produtos/detalhes/index.html")