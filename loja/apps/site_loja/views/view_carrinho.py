from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ...apps_administrador.produto.models import Produto
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
def adiciona_carrinho(request):
	if request.method == "POST":
		id_produto = request.POST.get('id_produto')
		qtd = request.POST.get('qtd')

		produto = Produto.objects.filter(id__gte=id_produto).first()

		if int(qtd) > int(produto.quantidade):
			return JsonResponse("Produto não tem esse total de quantidade", status=400, content_type="application/json")

		if produto.desconto is not None and produto.desconto != "":
			valor = produto.valor - produto.desconto
		else:
			valor = produto.valor

		produto = {
			'id': produto.id,
			'nome': produto.nome,
			'imagem_principal': str(produto.imagem_principal),
			'valor': str(valor),
		}
		
		if produto:
			return JsonResponse(produto, status=200, content_type="application/json")
		else:
			return JsonResponse(False, status=400, content_type="application/json")

@login_required(login_url="/login")
def carrinho(request):
	if request.method == "GET":
		return render(request, "carrinho/index.html")