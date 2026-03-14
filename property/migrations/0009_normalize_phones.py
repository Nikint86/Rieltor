from django.db import migrations
import phonenumbers


def normalize_phones(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')

    flats = Flat.objects.all()

    for flat in flats.iterator():
        if flat.owners_phonenumber:
            try:
                parsed_phone = phonenumbers.parse(flat.owners_phonenumber, 'RU')
                if phonenumbers.is_valid_number(parsed_phone):
                    flat.owner_pure_phone = parsed_phone
                    flat.save(update_fields=['owner_pure_phone'])
            except:
                pass


def normalize_phones_reverse(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Flat.objects.all().update(owner_pure_phone=None)


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0008_flat_owner_pure_phone'),
    ]

    operations = [
        migrations.RunPython(normalize_phones, normalize_phones_reverse),
    ]