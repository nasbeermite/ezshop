# Generated by Django 4.1.13 on 2024-03-11 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0012_salesbystaffitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salebystaffservice',
            name='employee',
        ),
    ]
