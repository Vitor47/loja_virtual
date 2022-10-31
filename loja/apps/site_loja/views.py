from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from loja.apps.apps_administrador.produto.models import Produto, ProdutoCategoria
from loja.apps.apps_administrador.banner.models import Banner


def home(request):
    if request.method == "GET":
        banners = Banner.objects.filter(status=True).order_by('-id')
        categorias_produtos = ProdutoCategoria.objects.all().order_by('-id')
        ofertas = Produto.objects.filter(tipo_id=1, status=True).order_by('-id')[:10]
        novidades = Produto.objects.filter(tipo_id=2, status=True).order_by('-id')[:10]
        return render(request, "home/index.html", {'banners': banners, 'categorias_produtos': categorias_produtos, 'ofertas':ofertas ,'novidades': novidades})

def produtos(request):
    if request.method == "GET":
        return render(request, "produtos/index.html")

def detalhes_produto(request):
    if request.method == "GET":
        return render(request, "produtos/detalhes/index.html")

def login(request):
    if request.method == "GET":
        return render(request, "conta/index.html")

def create_count(request):
    if request.method == "GET":
        return render(request, "conta/create_counta/index.html")