from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "age", "description", "available", "price", "image"]
        labels = {
            "name": "Nome",
            "age": "Idade (anos)",
            "description": "Descrição",
            "available": "Disponível para venda",
            "price": "Preço (R$)",
            "image": "Foto",
        }