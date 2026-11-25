from django.shortcuts import render, redirect
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)

from .models import Pet
from .forms import PetForm


@require_GET
def pet_list(request):
    """Lista apenas os pets que estão disponíveis."""
    petlist = []
    for item in Pet.objects.all():
        if item.available:
            petlist.append(item)
    context = {
        "pets": petlist,
    }
    return render(request, 'petlist.html', context)


@require_GET
def pet_detail(request, pet_id):
    """Exibe os detalhes de um pet."""
    context = {
        "pet": Pet.objects.get(id=pet_id),
    }
    return render(request, 'petdetail.html', context)


@require_http_methods(["GET", "POST"])
def create_pet(request):
    """GET: mostra o formulário vazio. POST: valida e salva o novo pet."""
    form = PetForm()
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pet-list')
    context = {
        "form": form,
    }
    return render(request, 'createpet.html', context)


@require_http_methods(["GET", "POST"])
def update_pet(request, pet_id):
    """GET: mostra o formulário preenchido. POST: valida e atualiza o pet."""
    pet = Pet.objects.get(id=pet_id)
    form = PetForm(instance=pet)
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet-list')
    context = {
        "pet": pet,
        "form": form,
    }
    return render(request, 'updatepet.html', context)


@require_POST
def delete_pet(request, pet_id):
    """Exclui um pet. Aceita apenas POST, pois altera dados."""
    Pet.objects.get(id=pet_id).delete()
    return redirect('pet-list')