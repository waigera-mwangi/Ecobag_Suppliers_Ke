# Generated by Django 4.1.2 on 2023-06-08 12:34

from django.db import migrations
import finance.models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_payment_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='phone_number',
            field=finance.models.CustomPhoneNumberField(max_length=128, null=True, region=None),
        ),
    ]
