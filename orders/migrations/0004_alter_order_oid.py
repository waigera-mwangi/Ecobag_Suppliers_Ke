# Generated by Django 4.1.2 on 2023-02-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_total_price_order_amount_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='oid',
            field=models.IntegerField(blank=True, max_length=50),
        ),
    ]
