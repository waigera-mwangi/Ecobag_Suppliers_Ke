# Generated by Django 4.1.2 on 2023-06-08 05:50

from django.db import migrations
import finance.models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='phone_number',
            field=finance.models.CustomPhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]
