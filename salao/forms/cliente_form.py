from django import forms
from ..models import cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = cliente.Cliente
        fields = ['nome','telefone','email']
