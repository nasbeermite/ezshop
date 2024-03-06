# Generated by Django 4.1.13 on 2024-03-06 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0050_remove_role_modules_role_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]