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
            for item_category in categoria_slug:
                categoria = ProdutoCategoria.objects.get(slug=item_category)

                list_products = Produto.objects.filter(categoria_id=categoria.id, status=True).exclude(quantidade=0).order_by('-id')
                for produto in list_products:
                    produto = {
                        'id': produto.id,
                        'nome': produto.nome,
                        'valor': produto.valor,
                        'imagem_principal': produto.imagem_principal
                    }
                    products.append(produto)

            context = {}
            context['produtos'] = products
            context['categorias'] = list_categorys
            return TemplateResponse(request, "produtos/index.html", context)

        valor_checkbox = request.GET.get('valor')
        if valor_checkbox is not None:
            products = []
            if valor_checkbox == "maior_100":
                for produto in list_products:
                    if produto.valor >= 100.00:
                        produto = {
                            'id': produto.id,
                            'nome': produto.nome,
                            'valor': produto.valor,
                            'imagem_principal': produto.imagem_principal
                        }
                        products.append(produto)
            elif valor_checkbox == "menor_100":
                for produto in list_products:
                    if produto.valor < 100.00:
                        produto = {
                            'id': produto.id,
                            'nome': produto.nome,
                            'valor': produto.valor,
                            'imagem_principal': produto.imagem_principal
                        }
                        products.append(produto)

            context = {}
            context['produtos'] = products
            context['categorias'] = list_categorys
            return TemplateResponse(request, "produtos/index.html", context)


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