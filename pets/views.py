from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (
    require_GET,
    require_POST,
    require_http_methods,
)

from .forms import PetForm
from .models import Pet


@require_GET
def pet_list(request):
    """Lista apenas os pets disponíveis."""
    pets = Pet.objects.filter(available=True).order_by('name')
    return render(request, 'petlist.html', {'pets': pets})


@require_GET
def pet_detail(request, pet_id):
    """Exibe os detalhes de um pet ou retorna 404."""
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'petdetail.html', {'pet': pet})


@require_http_methods(["GET", "POST"])
def create_pet(request):
    """GET: formulário vazio. POST: valida e cria o pet."""
    form = PetForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        pet = form.save()
        messages.success(request, f'Pet "{pet.name}" cadastrado com sucesso.')
        return redirect('pet-list')
    return render(request, 'createpet.html', {'form': form})


@require_http_methods(["GET", "POST"])
def update_pet(request, pet_id):
    """GET: formulário preenchido. POST: valida e atualiza o pet."""
    pet = get_object_or_404(Pet, id=pet_id)
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f'Pet "{pet.name}" atualizado com sucesso.')
        return redirect('pet-detail', pet_id=pet.id)
    return render(request, 'updatepet.html', {'pet': pet, 'form': form})


@require_POST
def delete_pet(request, pet_id):
    """Exclui um pet apenas via POST com proteção CSRF."""
    pet = get_object_or_404(Pet, id=pet_id)
    pet_name = pet.name
    pet.delete()
    messages.info(request, f'Pet "{pet_name}" removido.')
    return redirect('pet-list')