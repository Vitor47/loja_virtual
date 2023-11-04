from django import forms
from django.contrib.auth.models import User
from ...admin.cliente.models import Cliente, Endereco


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]


class CreateClienteForm(forms.ModelForm):
    telefone = forms.CharField(required=True)
    cpf_cnpj = forms.CharField(required=True)
    data_nascimento = forms.DateField(required=True)

    class Meta:
        model = Cliente
        fields = ["telefone", "cpf_cnpj", "data_nascimento"]


class CreateClienteEnderecoForm(forms.ModelForm):
    cep = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    bairro = forms.CharField(required=False)
    logradouro = forms.CharField(required=True)
    nr_casa = forms.IntegerField(required=False)

    class Meta:
        model = Endereco
        fields = ["cep", "estado", "cidade", "bairro", "logradouro", "nr_casa"]
