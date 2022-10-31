from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def home(request):
    if request.method == "GET":
        return render(request, "home/index.html")

def produtos(request):
    if request.method == "GET":
        return render(request, "produtos/index.html")

def detalhes_produto(request):
    if request.method == "GET":
        return render(request, "produtos/detalhes/index.html")

def login(request):
    if request.method == "GET":
        return render(request, "conta/login/index.html")

def create_count(request):
    if request.method == "GET":
        return render(request, "conta/create_counta/index.html")