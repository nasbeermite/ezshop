# Generated by Django 4.1.13 on 2024-03-01 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0036_remove_businessprofile_shop_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='ezshopapp.shop'),
        ),
    ]
