# Generated by Django 4.1.3 on 2023-02-22 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BentTree_API', '0005_rename_aparment_id_lease_apartment_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartment',
            old_name='max_occupancy',
            new_name='bedrooms',
        ),
    ]