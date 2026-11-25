from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=150, default="")
    age = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, default="")
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="pets/", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name