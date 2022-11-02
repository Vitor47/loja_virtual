from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from loja.apps.apps_administrador.produto.models import Produto, ProdutoCategoria
from loja.apps.apps_administrador.banner.models import Banner


def home(request):
    if request.method == "GET":
        banners = Banner.objects.filter(status=True).order_by('-id')
        categorias_produtos = ProdutoCategoria.objects.all().order_by('-id')
        ofertas = Produto.objects.filter(tipo_id=1, status=True).exclude(quantidade=0).order_by('-id')[:10]
        novidades = Produto.objects.filter(tipo_id=2, status=True).exclude(quantidade=0).order_by('-id')[:10]
        return render(request, "home/index.html", {'banners': banners, 'categorias_produtos': categorias_produtos, 'ofertas':ofertas ,'novidades': novidades})