# Generated by Django 4.1.2 on 2023-03-25 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickupstation',
            name='users',
        ),
    ]