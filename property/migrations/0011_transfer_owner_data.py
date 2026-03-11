from django.db import migrations
import phonenumbers


def transfer_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    flats = Flat.objects.all()
    total_flats = flats.count()
    created_count = 0
    found_count = 0
    error_count = 0

    print(f"\nНачинаем перенос данных о собственниках...")
    print(f"Всего квартир: {total_flats}")

    for i, flat in enumerate(flats.iterator(), 1):
        # Прогресс
        if i % 100 == 0:
            print(f"Обработано {i}/{total_flats} квартир")

        if not flat.owner:
            continue

        owner_data = {
            'name': flat.owner,
            'phonenumber': flat.owners_phonenumber or '',
            'pure_phone': flat.owner_pure_phone,
        }

        owner, created = Owner.objects.get_or_create(
            pure_phone=flat.owner_pure_phone if flat.owner_pure_phone else None,
            defaults={
                'name': flat.owner,
                'phonenumber': flat.owners_phonenumber or '',
            }
        )

        if created:
            created_count += 1
            if owner.name != flat.owner:
                owner.name = flat.owner
            if owner.phonenumber != flat.owners_phonenumber:
                owner.phonenumber = flat.owners_phonenumber or ''
            if not owner.pure_phone and flat.owner_pure_phone:
                owner.pure_phone = flat.owner_pure_phone
            owner.save()
        else:
            found_count += 1
            need_update = False

            if owner.name != flat.owner:
                owner.name = flat.owner
                need_update = True

            if flat.owners_phonenumber and owner.phonenumber != flat.owners_phonenumber:
                owner.phonenumber = flat.owners_phonenumber
                need_update = True

            if flat.owner_pure_phone and not owner.pure_phone:
                owner.pure_phone = flat.owner_pure_phone
                need_update = True

            if need_update:
                owner.save()

        owner.flats.add(flat)

    print(f"\n{'=' * 50}")
    print(f"ПЕРЕНОС ДАННЫХ ЗАВЕРШЕН")
    print(f"{'=' * 50}")
    print(f"Всего обработано квартир: {total_flats}")
    print(f"Создано новых собственников: {created_count}")
    print(f"Найдено существующих собственников: {found_count}")
    print(f"Ошибок: {error_count}")
    print(f"Всего собственников в базе: {Owner.objects.count()}")
    print(f"{'=' * 50}")


def reverse_transfer(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')

    count = Owner.objects.count()
    Owner.objects.all().delete()

    print(f"\nУдалено {count} собственников")


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0010_alter_flat_owner_pure_phone_owner'),
    ]

    operations = [
        migrations.RunPython(transfer_owners, reverse_transfer),
    ]