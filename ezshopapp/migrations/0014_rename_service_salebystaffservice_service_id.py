# Generated by Django 4.1.13 on 2024-03-11 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0013_remove_salebystaffservice_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salebystaffservice',
            old_name='service',
            new_name='service_id',
        ),
    ]
