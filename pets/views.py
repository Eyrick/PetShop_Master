from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ClassifiedPetForm as PetForm
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

from uuid import uuid4
from django.db import IntegrityError, transaction
from .forms import AdoptionForm, ChatForm
from .models import AdoptionRequest, ChatMessage


def visitor_token(request):
    if 'petmaster_visitor' not in request.session:
        request.session['petmaster_visitor'] = uuid4().hex
    return request.session['petmaster_visitor']


def adoption(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    visitor = visitor_token(request)
    form = AdoptionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                # Write first to serialize queue changes on SQLite.
                if not Pet.objects.filter(pk=pet.pk, available=True).update(available=True) or pet.adoption_requests.filter(status="completed").exists():
                    form.add_error(None, 'Pet indisponível.')
                else:
                    AdoptionRequest.objects.create(pet=pet, visitor=visitor, **form.cleaned_data)
                    return redirect('adoption', pet_id=pet.pk)
        except IntegrityError:
            form.add_error(None, 'Já existe uma solicitação ativa nesta sessão.')
    waiting = pet.adoption_requests.filter(status='waiting')
    own = pet.adoption_requests.filter(visitor=visitor).last()
    position = None
    if own and own.status == 'waiting':
        ids = list(waiting.values_list("pk", flat=True))
        if own.pk in ids:
            position = ids.index(own.pk) + 1
    return render(request, 'adoption.html', {'pet': pet, 'form': form, 'own': own, 'position': position})


def chat(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    visitor = visitor_token(request)
    form = ChatForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ChatMessage.objects.create(pet=pet, visitor=visitor, body=form.cleaned_data['body'])
        return redirect('pet-chat', pet_id=pet.pk)
    return render(request, 'chat.html', {'pet': pet, 'form': form, 'history': ChatMessage.objects.filter(pet=pet, visitor=visitor)})
