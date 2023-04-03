# Generated by Django 4.1.2 on 2023-03-25 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_alter_order_date_ordered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PickUpStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shipping.location')),
                ('users', models.ManyToManyField(related_name='pickup_stations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPickUpStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('station', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shipping.pickupstation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_up_stations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateTimeField(auto_now_add=True, verbose_name='shipped_date')),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('OFD', 'Out For Delivery'), ('DL', 'Delivered')], default='PD', max_length=3, verbose_name='status')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments_as_driver', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('service_provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipments_as_service_provider', to=settings.AUTH_USER_MODEL)),
                ('station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shipping.userpickupstation')),
            ],
        ),
    ]