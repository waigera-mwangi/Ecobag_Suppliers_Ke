# Generated by Django 4.1.2 on 2023-06-07 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='service_provider',
        ),
    ]
