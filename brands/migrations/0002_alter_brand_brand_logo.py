# Generated by Django 4.1.2 on 2023-06-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_logo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
