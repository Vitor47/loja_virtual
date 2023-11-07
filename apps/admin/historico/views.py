# Retornar templates
from django.shortcuts import render

# Django Decorators
from django.contrib.auth.decorators import login_required, permission_required

# Logs
from django.contrib.admin.models import LogEntry

# Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Permissões
from ..decorators import manager_required


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
def historico(request):
    if request.method == "GET":
        historico = LogEntry.objects.all().order_by("-id")

        paginator = Paginator(historico, 10)
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1
        try:
            history = paginator.page(page)
        except (EmptyPage, InvalidPage):
            history = paginator.page(paginator.num_pages)
        return render(request, "historico/index.html", {"historico": history})
