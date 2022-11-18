from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
#Retornar templates
from django.shortcuts import redirect, render
#Importa demais coisas
from django.contrib.auth.models import User
#Permissões
from ..decorators import manager_required

@login_required(login_url="/admin")
@manager_required(login_url="/admin")
def dashboard(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        return render(request, "dashboard/index.html", {'usuario': user})
    else:
        return redirect('/admin')