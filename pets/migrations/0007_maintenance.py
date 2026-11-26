from django.db import migrations, models
import django.db.models.deletion


def seed_catalog(apps, schema_editor):
    Category = apps.get_model('pets', 'Category')
    Breed = apps.get_model('pets', 'Breed')
    Pet = apps.get_model('pets', 'Pet')
    catalog = {'Cachorro': ['Golden Retriever', 'Bulldog Francês', 'Shih Tzu', 'Spitz Alemão', 'Labrador', 'Rottweiler', 'Poodle', 'Sem raça definida'], 'Gato': ['Siamês', 'Persa', 'Maine Coon', 'Sem raça definida'], 'Ave': ['Calopsita Lutino', 'Canário', 'Periquito'], 'Coelho': ['Mini Lop', 'Sem raça definida']}
    known = {'Thor - Golden Retriever': 'Golden Retriever', 'Luna - Gata Siamês': 'Siamês', 'Max - Bulldog Francês': 'Bulldog Francês', 'Mel - Shih Tzu': 'Shih Tzu', 'Bento - Calopsita Lutino': 'Calopsita Lutino', 'Nina - Spitz Alemão': 'Spitz Alemão', 'Pipoca - Coelho Mini Lop': 'Mini Lop', 'Bob - Labrador (Vendido)': 'Labrador'}
    for category, breeds in catalog.items():
        cat, _ = Category.objects.get_or_create(name=category)
        for name in breeds:
            Breed.objects.get_or_create(category=cat, name=name)
    for name, breed in known.items():
        Pet.objects.filter(name=name, breed__isnull=True).update(breed=Breed.objects.get(name=breed))


class Migration(migrations.Migration):
    dependencies = [('pets', '0006_pet_description_alter_pet_age_alter_pet_id_and_more')]
    operations = [
        migrations.CreateModel(name='Category', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80, unique=True))]),
        migrations.CreateModel(name='Breed', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80)), ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pets.category'))]),
        migrations.AddConstraint(model_name='breed', constraint=models.UniqueConstraint(fields=('category', 'name'), name='unique_category_breed')),
        migrations.AddField(model_name='pet', name='breed', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pets.breed')),
        migrations.CreateModel(name='AdoptionRequest', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('visitor', models.CharField(editable=False, max_length=64)), ('name', models.CharField(max_length=100)), ('contact', models.EmailField(max_length=254)), ('created_at', models.DateTimeField(auto_now_add=True)), ('status', models.CharField(choices=[('waiting','Aguardando'),('failed','Não concluída'),('completed','Concluída')], default='waiting', max_length=12)), ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adoption_requests', to='pets.pet'))], options={'ordering':['created_at','pk']}),
        migrations.AddConstraint(model_name='adoptionrequest', constraint=models.UniqueConstraint(fields=('pet','visitor'), condition=models.Q(status='waiting'), name='one_waiting_per_visitor')),
        migrations.AddConstraint(model_name='adoptionrequest', constraint=models.UniqueConstraint(fields=('pet',), condition=models.Q(status='completed'), name='one_completed_per_pet')),
        migrations.CreateModel(name='ChatMessage', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('visitor', models.CharField(editable=False, max_length=64)), ('body', models.CharField(max_length=1000)), ('from_shop', models.BooleanField(default=False)), ('created_at', models.DateTimeField(auto_now_add=True)), ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet'))], options={'ordering':['created_at','pk']}),
        migrations.RunPython(seed_catalog, migrations.RunPython.noop),
    ]
