from django.db import migrations


def transfer_owners(apps, schema_editor):
    Flat = apps.get_model('property', 'Flat')
    Owner = apps.get_model('property', 'Owner')

    flats = Flat.objects.all()

    for flat in flats.iterator():
        if not flat.owner:
            continue

        owner, created = Owner.objects.get_or_create(
            pure_phone=flat.owner_pure_phone if flat.owner_pure_phone else None,
            defaults={
                'name': flat.owner,
                'phonenumber': flat.owners_phonenumber or '',
            }
        )

        if not created:
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


def reverse_transfer(apps, schema_editor):
    Owner = apps.get_model('property', 'Owner')
    Owner.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('property', '0010_alter_flat_owner_pure_phone_owner'),
    ]

    operations = [
        migrations.RunPython(transfer_owners, reverse_transfer),
    ]