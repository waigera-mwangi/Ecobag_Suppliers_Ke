# Generated by Django 4.1.2 on 2023-03-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_options_remove_order_amount_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date ordered'),
        ),
    ]
