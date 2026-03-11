from django.db import migrations


def link_owners_to_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    flats = Flat.objects.all()
    total_flats = flats.count()
    linked_count = 0

    print(f"\nНачинаем связывание собственников с квартирами...")
    print(f"Всего квартир: {total_flats}")

    for i, flat in enumerate(flats.iterator(), 1):
        if i % 100 == 0:
            print(f"Обработано {i}/{total_flats} квартир")

        owner = None
        if flat.owner_pure_phone:
            owner = Owner.objects.filter(pure_phone=flat.owner_pure_phone).first()

        if not owner and flat.owners_phonenumber:
            owner = Owner.objects.filter(
                phonenumber=flat.owners_phonenumber,
                name=flat.owner
            ).first()

        if not owner and flat.owner:
            owner = Owner.objects.filter(name=flat.owner).first()

        if owner:
            owner.flats.add(flat)
            linked_count += 1

    print(f"\n{'=' * 50}")
    print(f"СВЯЗЫВАНИЕ ЗАВЕРШЕНО")
    print(f"{'=' * 50}")
    print(f"Всего обработано квартир: {total_flats}")
    print(f"Связано с собственниками: {linked_count}")
    print(f"Не найдено собственников: {total_flats - linked_count}")
    print(f"{'=' * 50}")


def reverse_link_owners_to_flats(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    for flat in Flat.objects.all():
        flat.owners.clear()

    print(f"\nВсе связи между собственниками и квартирами очищены")


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0011_transfer_owner_data'),
    ]

    operations = [
        migrations.RunPython(link_owners_to_flats, reverse_link_owners_to_flats),
    ]
