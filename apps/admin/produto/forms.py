from django.forms import ModelForm, Select
from .models import ProdutoDiamentro


class FormCodigoServico(ModelForm):
    class Meta:
        model = ProdutoDiamentro
        required = (True,)
        fields = ["nCdServico"]
        widgets = {
            "nCdServico": Select(attrs={"class": "form-control"}),
        }


class FormCodigoFormato(ModelForm):
    class Meta:
        model = ProdutoDiamentro
        required = (True,)
        fields = ["nCdFormato"]
        widgets = {
            "nCdFormato": Select(attrs={"class": "form-control"}),
        }
