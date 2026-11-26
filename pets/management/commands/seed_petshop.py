from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from pets.models import Pet, Breed
from pets.catalog import SEED_BREEDS

SEED_PETS = [
    {
        "name": "Thor - Golden Retriever",
        "age": 1,
        "price": Decimal("2400.00"),
        "available": True,
        "description": "Filhote dócil, vacinado (V10 e antirrábica) e vermifugado.",
        "filename": "thor-golden.png",
        "bg_color": (255, 241, 214),
        "accent_color": (217, 138, 43),
    },
    {
        "name": "Luna - Gata Siamês",
        "age": 1,
        "price": Decimal("950.00"),
        "available": True,
        "description": "Gata carinhosa, acostumada com caixa de areia e castrada.",
        "filename": "luna-siames.png",
        "bg_color": (232, 240, 254),
        "accent_color": (66, 103, 178),
    },
    {
        "name": "Max - Bulldog Francês",
        "age": 2,
        "price": Decimal("3200.00"),
        "available": True,
        "description": "Porte compacto, ideal para apartamento, com pedigree e microchip.",
        "filename": "max-bulldog.png",
        "bg_color": (237, 231, 246),
        "accent_color": (103, 58, 183),
    },
    {
        "name": "Mel - Shih Tzu",
        "age": 1,
        "price": Decimal("1850.00"),
        "available": True,
        "description": "Pelagem bicolor, calma e sociável com crianças e outros animais.",
        "filename": "mel-shihtzu.png",
        "bg_color": (252, 228, 236),
        "accent_color": (194, 24, 91),
    },
    {
        "name": "Bento - Calopsita Lutino",
        "age": 1,
        "price": Decimal("380.00"),
        "available": True,
        "description": "Ave mansa criada na papinha, acompanha anilha de identificação.",
        "filename": "bento-calopsita.png",
        "bg_color": (255, 249, 196),
        "accent_color": (245, 166, 35),
    },
    {
        "name": "Nina - Spitz Alemão",
        "age": 2,
        "price": Decimal("3800.00"),
        "available": True,
        "description": "Spitz anão cor creme, vacinação em dia e atestado veterinário.",
        "filename": "nina-spitz.png",
        "bg_color": (224, 242, 241),
        "accent_color": (0, 121, 107),
    },
    {
        "name": "Pipoca - Coelho Mini Lop",
        "age": 1,
        "price": Decimal("290.00"),
        "available": True,
        "description": "Coelho de orelhas caídas, dócil e adaptado à ração extrusada.",
        "filename": "pipoca-coelho.png",
        "bg_color": (232, 245, 233),
        "accent_color": (46, 125, 50),
    },
    {
        "name": "Bob - Labrador (Vendido)",
        "age": 3,
        "price": Decimal("1900.00"),
        "available": False,
        "description": "Registro mantido no banco para testar filtro de indisponíveis.",
        "filename": "bob-labrador.png",
        "bg_color": (236, 239, 241),
        "accent_color": (84, 110, 122),
    },
]


def build_pet_card_image(bg_color, accent_color):
    """Gera uma imagem PNG 600x400 limpa com emblema de patinha."""
    img = Image.new("RGB", (600, 400), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Moldura e círculo central
    draw.rounded_rectangle((28, 28, 572, 372), radius=24, outline=accent_color, width=6)
    draw.ellipse((200, 100, 400, 300), fill=(255, 255, 255))

    # Emblema de patinha estilizada
    draw.ellipse((255, 200, 345, 270), fill=accent_color)
    draw.ellipse((232, 158, 268, 198), fill=accent_color)
    draw.ellipse((270, 134, 304, 178), fill=accent_color)
    draw.ellipse((308, 138, 342, 180), fill=accent_color)
    draw.ellipse((338, 166, 370, 204), fill=accent_color)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


class Command(BaseCommand):
    help = "Popula o catálogo do PetShop Master com novos pets e imagens válidas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Remove todos os pets existentes antes de popular.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            for existing in Pet.objects.all():
                if existing.image:
                    existing.image.delete(save=False)
            deleted, _ = Pet.objects.all().delete()
            self.stdout.write(f"Removidos {deleted} registro(s) antigo(s).")

        created_count = 0
        for item, breed_name in zip(SEED_PETS, SEED_BREEDS):
            pet, created = Pet.objects.get_or_create(
                name=item["name"],
                defaults={
                    "breed": Breed.objects.get(name=breed_name),
                    "age": item["age"],
                    "price": item["price"],
                    "available": item["available"],
                    "description": item["description"],
                },
            )
            if created or not pet.image:
                png_bytes = build_pet_card_image(
                    item["bg_color"], item["accent_color"]
                )
                pet.image.save(item["filename"], ContentFile(png_bytes), save=True)
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed concluído: {created_count} pet(s) criado(s). Total no catálogo: {Pet.objects.count()}."
            )
        )
        