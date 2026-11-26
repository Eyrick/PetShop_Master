from django.db import models


class Pet(models.Model):
    breed = models.ForeignKey("Breed", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=150, default="")
    age = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="pets/", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Breed(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['category', 'name'], name='unique_category_breed')]

    def __str__(self):
        return self.name


class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    visitor = models.CharField(max_length=64, editable=False)
    name = models.CharField(max_length=100)
    contact = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=[('waiting', 'Aguardando'), ('failed', 'Não concluída'), ('completed', 'Concluída')], default='waiting')

    class Meta:
        ordering = ['created_at', 'pk']
        constraints = [models.UniqueConstraint(fields=['pet', 'visitor'], condition=models.Q(status='waiting'), name='one_waiting_per_visitor'), models.UniqueConstraint(fields=['pet'], condition=models.Q(status='completed'), name='one_completed_per_pet')]


class ChatMessage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    visitor = models.CharField(max_length=64, editable=False)
    body = models.CharField(max_length=1000)
    from_shop = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'pk']
