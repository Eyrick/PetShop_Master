from django.contrib import admin, messages
from django.db import transaction
from django import forms
from .models import Pet, Category, Breed, AdoptionRequest, ChatMessage
from .forms import ClassifiedPetForm


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    form = ClassifiedPetForm


admin.site.register(Category)
admin.site.register(Breed)


@admin.register(AdoptionRequest)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('pet', 'name', 'contact', 'created_at', 'status')
    list_filter = ('status', 'pet')
    readonly_fields = ('pet', 'name', 'contact', 'created_at', 'status')
    actions = ['fail_first', 'complete_first']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def advance(self, request, queryset, status):
        if queryset.count() != 1:
            self.message_user(request, 'Selecione uma solicitação por vez.', messages.WARNING)
            return
        for entry in queryset.order_by('created_at', 'pk'):
            with transaction.atomic():
                if not Pet.objects.filter(pk=entry.pet_id, available=True).update(available=True):
                    self.message_user(request, 'Pet indisponível.', messages.WARNING)
                    continue
                first = AdoptionRequest.objects.filter(pet_id=entry.pet_id, status='waiting').first()
                if not first or first.pk != entry.pk:
                    self.message_user(request, 'Selecione apenas o primeiro interessado da fila.', messages.WARNING)
                    continue
                first.status = status
                first.save(update_fields=['status'])
                if status == 'completed':
                    Pet.objects.filter(pk=entry.pet_id).update(available=False)
                    AdoptionRequest.objects.filter(pet_id=entry.pet_id, status='waiting').update(status='failed')

    @admin.action(description='Marcar primeira tentativa como não concluída')
    def fail_first(self, request, queryset):
        self.advance(request, queryset, 'failed')

    @admin.action(description='Concluir adoção do primeiro interessado')
    def complete_first(self, request, queryset):
        self.advance(request, queryset, 'completed')


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(label='Responder ao cliente', required=False, max_length=1000, widget=forms.Textarea)

    class Meta:
        model = ChatMessage
        fields = []


@admin.register(ChatMessage)
class ChatAdmin(admin.ModelAdmin):
    form = ReplyForm
    fields = ('pet', 'visitor', 'body', 'from_shop', 'created_at', 'reply')
    readonly_fields = ('pet', 'visitor', 'body', 'from_shop', 'created_at')
    list_display = ('pet', 'visitor', 'body', 'from_shop', 'created_at')
    list_filter = ('pet', 'from_shop')
    search_fields = ('visitor', 'body')

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        reply = form.cleaned_data.get('reply')
        if reply:
            ChatMessage.objects.create(pet=obj.pet, visitor=obj.visitor, body=reply, from_shop=True)
