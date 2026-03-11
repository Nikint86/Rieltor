from django.db import migrations
import phonenumbers
import logging

logger = logging.getLogger(__name__)


def normalize_phones(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    flats = Flat.objects.all()
    total_flats = flats.count()
    updated_count = 0
    error_count = 0
    invalid_count = 0

    print(f"\nНачинаем обработку {total_flats} квартир...")

    for i, flat in enumerate(flats, 1):
        if i % 100 == 0:
            print(f"Обработано {i}/{total_flats} квартир")

        if flat.owners_phonenumber:
            try:
                parsed_phone = phonenumbers.parse(flat.owners_phonenumber, 'RU')

                if phonenumbers.is_valid_number(parsed_phone):
                    flat.owner_pure_phone = parsed_phone
                    flat.save(update_fields=['owner_pure_phone'])
                    updated_count += 1
                else:
                    invalid_count += 1
                    logger.warning(f"Невалидный номер: '{flat.owners_phonenumber}' (квартира ID: {flat.id})")

            except phonenumbers.NumberParseException as e:
                error_count += 1
                logger.error(f"Ошибка парсинга номера '{flat.owners_phonenumber}': {e} (квартира ID: {flat.id})")
            except Exception as e:
                error_count += 1
                logger.error(
                    f"Неизвестная ошибка при обработке номера '{flat.owners_phonenumber}': {e} (квартира ID: {flat.id})")

    # Выводим статистику
    print(f"\n{'=' * 50}")
    print(f"Обработка завершена!")
    print(f"Всего квартир: {total_flats}")
    print(f"Успешно нормализовано: {updated_count}")
    print(f"Невалидных номеров (но распарсено): {invalid_count}")
    print(f"Ошибок парсинга: {error_count}")
    print(f"Пустых номеров: {total_flats - updated_count - invalid_count - error_count}")
    print(f"{'=' * 50}")


def normalize_phones_reverse(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    updated = Flat.objects.all().update(owner_pure_phone=None)
    print(f"\nПоле owner_pure_phone очищено у {updated} квартир")


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0008_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(normalize_phones, normalize_phones_reverse),
    ]