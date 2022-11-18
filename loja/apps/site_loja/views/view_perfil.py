from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from ...apps_administrador.cliente.models import Cliente, Endereco

@login_required(login_url="/login")
def perfil_site(request):
	if request.user.is_authenticated:
		user = User.objects.get(id=request.user.id)
		if request.method == "GET":
			cliente = Cliente.objects.filter(user_cliente_id=user.id).first()
			if cliente:
				if len(cliente.cpf_cnpj) == 11:
					cpf_cnpj = f'{cliente.cpf_cnpj[0:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:11]}'
				elif len(cliente.cpf_cnpj) == 14:
					'55.555.555/5555-55'
					cpf_cnpj = f'{cliente.cpf_cnpj[0:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:14]}'

				telefone = f'({cliente.telefone[0:2]}) {cliente.telefone[2:7]}-{cliente.telefone[7:11]}'
				data_nascimento = cliente.data_nascimento
				avatar = cliente.avatar
			else:
				cpf_cnpj = ""
				telefone = ""
				data_nascimento = ""
				avatar = " "

			endereco = Endereco.objects.filter(user_cliente_id=user.id).first()
			if endereco:
				cep = endereco.cep
				estado = endereco.estado
				cidade = endereco.cidade
				logradouro = endereco.logradouro
				nr_casa = endereco.nr_casa
			else:
				cep = ""
				estado = ""
				cidade = ""
				logradouro = ""
				nr_casa = ""

			perfil = {
				'nome': user.first_name,
				'email': user.email,
				'telefone': telefone,
				'cpf_cnpj': cpf_cnpj,
				'data_nascimento': data_nascimento,
				'avatar': avatar,
				'cep': cep,
				'estado': estado,
				'cidade': cidade,
				'logradouro': logradouro,
				'nr_casa': nr_casa,

			}
			return render(request, "perfil_site/index.html", {'perfil': perfil})
		elif request.method == "POST":
			try:
				cliente = Cliente.objects.filter(user_cliente_id=request.user.id).first()
				if cliente:
					image = request.POST.get('image')
					print(image)
					for i in range(5):
						if i == int(image):
							cliente.avatar = f'ava{image}.webp'

					cliente.save()
					response = {
						'message': True,
					}
					return JsonResponse(response, status=200, content_type="application/json")
				else:
					response = {
						'message': False,
					}
					return JsonResponse(response, status=400, content_type="application/json")
				
			except Exception as e:
				response = {
					'message': False,
				}
				return JsonResponse(response, status=400, content_type="application/json")