from django.shortcuts import render

def pagamento(request):
    if request.method == "GET":
        return render(request, "pagamento/index.html", {"pagamento": []})