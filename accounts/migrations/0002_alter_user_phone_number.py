# Generated by Django 4.1.2 on 2023-06-25 10:16

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=accounts.models.CustomPhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]
