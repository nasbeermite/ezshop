# Generated by Django 4.1.13 on 2024-03-11 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0017_salesbyadminitem_total_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SalesByStaffItem',
            new_name='SaleByStaffItem',
        ),
    ]