# Generated by Django 4.1.13 on 2024-03-05 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0048_modules_alter_module_name_alter_shop_num_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='modules',
        ),
        migrations.AddField(
            model_name='role',
            name='modules',
            field=models.CharField(choices=[('shop', 'Shop'), ('business', 'Business Profile'), ('employee', 'Employee'), ('sale', 'Sale & Day Closing'), ('role', 'Role'), ('expense-type', 'Expense Type'), ('receipt-transaction', 'Receipt Transaction'), ('payment-transaction', 'Payment Transaction'), ('service', 'Service'), ('product', 'Product'), ('employee-transaction', 'Employee Transaction'), ('daily-summary', 'Daily Summary'), ('bank', 'Bank Deposit')], max_length=50, null=True),
        ),
    ]