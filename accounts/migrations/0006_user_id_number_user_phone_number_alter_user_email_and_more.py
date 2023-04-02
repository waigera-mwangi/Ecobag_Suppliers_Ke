# Generated by Django 4.1.2 on 2023-04-02 00:43

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_brander_dispatch_driver_finance_inventory_supply_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_number',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=accounts.models.CustomPhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('DR', 'Driver'), ('FM', 'Finance Manager'), ('SM', 'Inventory Manager'), ('RD', 'Supplier'), ('CM', 'Customer'), ('MN', 'Manager'), ('BR', 'Brander'), ('DM', 'Dispatch Manager'), ('AD', 'Admin')], default='CM', max_length=2),
        ),
    ]
