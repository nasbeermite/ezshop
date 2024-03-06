# Generated by Django 4.1.13 on 2024-03-06 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0051_role_is_employee_alter_module_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='shop',
            name='password',
            field=models.CharField(default='password', max_length=100),
        ),
        migrations.AddField(
            model_name='shop',
            name='username',
            field=models.CharField(default='root', max_length=100),
        ),
    ]