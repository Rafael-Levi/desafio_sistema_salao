from django import forms

class RelatorioForm(forms.Form):
    start = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))
    end = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}))