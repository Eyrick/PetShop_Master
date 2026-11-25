from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PetForm
from .models import Pet


def pet_list(request):
    pets = Pet.objects.filter(available=True).order_by("id")
    return render(request, "petlist.html", {"pets": pets})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, "petdetail.html", {"pet": pet})


def create_pet(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pet-list")
    else:
        form = PetForm()
    return render(request, "createpet.html", {"form": form})


def update_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("pet-detail", pet_id=pet.id)
    else:
        form = PetForm(instance=pet)
    return render(request, "updatepet.html", {"form": form, "pet": pet})


@require_POST
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.delete()
    return redirect("pet-list")