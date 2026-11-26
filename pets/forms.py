from django import forms

from .models import Pet


class BasePetForm(forms.ModelForm):
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

from .models import Category, Breed


class ClassifiedPetForm(BasePetForm):
    category = forms.ModelChoiceField(queryset=Category.objects.order_by('name'), label='Categoria')
    breed = forms.ModelChoiceField(queryset=Breed.objects.select_related('category').order_by('name'), label='Raça')

    class Meta(BasePetForm.Meta):
        fields = ['name', 'category', 'breed', 'age', 'description', 'available', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.breed_id:
            self.initial['category'] = self.instance.breed.category_id
        self.fields['breed'].widget = BreedSelect(choices=self.fields['breed'].choices)

    def clean(self):
        data = super().clean()
        category, breed = data.get('category'), data.get('breed')
        if category and breed and breed.category_id != category.pk:
            self.add_error('breed', 'A raça não pertence à categoria selecionada.')
        return data


class BreedSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if hasattr(value, 'instance'):
            option['attrs']['data-category'] = value.instance.category_id
        return option


class AdoptionForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome')
    contact = forms.EmailField(label='E-mail para contato')


class ChatForm(forms.Form):
    body = forms.CharField(max_length=1000, label='Mensagem', widget=forms.Textarea(attrs={'rows': 3}))


PetForm = ClassifiedPetForm
