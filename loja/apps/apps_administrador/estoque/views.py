#Mensagens Template
from django.contrib import messages
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
#Retornar templates
from django.shortcuts import redirect, render
#Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

#Permissões

#from .models import Estoque

@login_required(login_url="/admin")
@permission_required('configuracao.view_configuracao')
def configuracao(request):
    if request.method == "GET":
        list_estoques = Estoque.objects.all().order_by('-id')
        return render(request, "estoque/index.html", {'estoques': list_estoques})