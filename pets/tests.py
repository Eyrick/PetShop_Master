import tempfile
from decimal import Decimal
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import PetForm
from .models import Pet


def make_test_image(name="pet.png"):
    buffer = BytesIO()
    Image.new("RGB", (40, 40), color=(100, 180, 220)).save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


class PetModelAndFormTest(TestCase):
    def test_pet_str_returns_name(self):
        pet = Pet.objects.create(
            name="Rex", age=2, price=Decimal("1250.00"), description="Muito ativo"
        )
        self.assertEqual(str(pet), "Rex")
        self.assertTrue(pet.available)

    def test_pet_form_valid(self):
        form = PetForm(
            data={
                "name": "Maya",
                "age": 1,
                "description": "Filhote vacinada",
                "available": True,
                "price": "1500.50",
            }
        )
        self.assertTrue(form.is_valid())


class PetViewsTest(TestCase):
    def setUp(self):
        self.pet_available = Pet.objects.create(
            name="Bento",
            age=1,
            price=Decimal("400.00"),
            available=True,
            description="Disponível",
        )
        self.pet_sold = Pet.objects.create(
            name="Alfa",
            age=3,
            price=Decimal("900.00"),
            available=False,
            description="Já vendido",
        )

    def test_home_and_pet_list_show_only_available_pets(self):
        for route in ("home", "pet-list"):
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)
            pets = list(response.context["pets"])
            self.assertEqual(pets, [self.pet_available])

    def test_pet_detail_existing_and_not_found(self):
        ok_resp = self.client.get(
            reverse("pet-detail", args=[self.pet_available.id])
        )
        self.assertEqual(ok_resp.status_code, 200)
        self.assertContains(ok_resp, "Bento")

        not_found = self.client.get(reverse("pet-detail", args=[99999]))
        self.assertEqual(not_found.status_code, 404)

    def test_create_pet_get_and_post(self):
        get_resp = self.client.get(reverse("create-pet"))
        self.assertEqual(get_resp.status_code, 200)

        with tempfile.TemporaryDirectory() as tmp_media:
            with override_settings(MEDIA_ROOT=tmp_media):
                post_resp = self.client.post(
                    reverse("create-pet"),
                    data={
                        "name": "Lola",
                        "age": 2,
                        "description": "Dócil",
                        "available": True,
                        "price": "1800.00",
                        "image": make_test_image("lola.png"),
                    },
                )
        self.assertRedirects(post_resp, reverse("pet-list"))
        self.assertTrue(Pet.objects.filter(name="Lola").exists())

    def test_create_pet_invalid_renders_form(self):
        resp = self.client.post(reverse("create-pet"), data={"name": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["form"].is_valid())

    def test_update_pet_get_post_and_404(self):
        url = reverse("update-pet", args=[self.pet_available.id])
        self.assertEqual(self.client.get(url).status_code, 200)

        resp = self.client.post(
            url,
            data={
                "name": "Bento Atualizado",
                "age": 2,
                "description": "Nova descrição",
                "available": True,
                "price": "450.00",
            },
        )
        self.assertRedirects(
            resp, reverse("pet-detail", args=[self.pet_available.id])
        )
        self.pet_available.refresh_from_db()
        self.assertEqual(self.pet_available.name, "Bento Atualizado")

        not_found = self.client.get(reverse("update-pet", args=[99999]))
        self.assertEqual(not_found.status_code, 404)

    def test_delete_pet_requires_post_and_deletes(self):
        url = reverse("delete-pet", args=[self.pet_available.id])
        self.assertEqual(self.client.get(url).status_code, 405)

        resp = self.client.post(url)
        self.assertRedirects(resp, reverse("pet-list"))
        self.assertFalse(Pet.objects.filter(id=self.pet_available.id).exists())

        not_found = self.client.post(reverse("delete-pet", args=[99999]))
        self.assertEqual(not_found.status_code, 404)


class SeedCommandTest(TestCase):
    def test_seed_petshop_creates_and_resets_catalog(self):
        with tempfile.TemporaryDirectory() as tmp_media:
            with override_settings(MEDIA_ROOT=tmp_media):
                call_command("seed_petshop")
                first_count = Pet.objects.count()
                self.assertEqual(first_count, 8)
                self.assertEqual(Pet.objects.filter(available=True).count(), 7)

                call_command("seed_petshop", reset=True)
                self.assertEqual(Pet.objects.count(), 8)