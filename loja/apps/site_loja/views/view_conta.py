from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == "GET":
        return render(request, "conta/index.html")