from django.db import migrations, models


def set_new_building(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    new_buildings = Flat.objects.filter(construction_year__gte=2015).update(new_building=True)
    old_buildings = Flat.objects.filter(construction_year__lt=2015).update(new_building=False)

    print(f'\nОбновлено {new_buildings} новостроек')
    print(f'Обновлено {old_buildings} старых зданий')
    print(f'Не заполнено: {Flat.objects.filter(construction_year__isnull=True).count()} квартир')


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