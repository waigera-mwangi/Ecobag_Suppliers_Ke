# Generated by Django 4.1.2 on 2023-07-01 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_alter_payment_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
