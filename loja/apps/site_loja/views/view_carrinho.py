from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def carrinho(request):
	if request.method == "GET":
		return render(request, "carrinho/index.html")