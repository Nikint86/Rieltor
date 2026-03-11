from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_link_owners_to_flats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flat',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='owners_phonenumber',
        ),
        migrations.RemoveField(
            model_name='flat',
            name='owner_pure_phone',
        ),
    ]
