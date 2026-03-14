from django.db import migrations


def set_new_building(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.filter(construction_year__gte=2015).update(new_building=True)
    Flat.objects.filter(construction_year__lt=2015).update(new_building=False)


def reverse_new_building(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.all().update(new_building=None)


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_flat_new_building'),
    ]

    operations = [
        migrations.RunPython(set_new_building, reverse_new_building),
    ]