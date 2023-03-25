from django.db import models
# from pkg_resources import _
from django.urls import reverse
from djmoney.models.fields import MoneyField
from moneyed import Money
from accounts.models import User, Customer


class Category(models.Model):
    name =  models.CharField(max_length=255, db_index=True)
    slug =  models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'product', on_delete=models.CASCADE,null = True,default='Gift_bag')
    name = models.CharField(max_length=120, unique=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Price', null=True)
    quantity = models.IntegerField(null=True)
    image = models.ImageField()
    created_date = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(('Updated'), auto_now=True, null=True)
    description = models.CharField(max_length=100, null=True)
    in_stock = models.BooleanField(default = True)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.name


# #
# class OrderPayment(models.Model):
#     transaction_id = models.CharField(max_length=250)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     mpesa = models.CharField(max_length=10, help_text="Mpesa Code e.g MXFTR432R5")
#     phone = models.IntegerField(blank=True, null=True)
#     # manager = models.ForeignKey(Finance Man, on_delete=models.CASCADE, null=True)
#     amount = models.FloatField(default=0.0)
#     confirmed = models.BooleanField(default=False, help_text="Means manager has confirmed payment")
#     updated = models.DateTimeField(('Updated'), auto_now=True, null=True)
#     created = models.DateTimeField(('Created'), auto_now_add=True, null=True)


#
# class Customer(User):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=120, unique=True)
#     address = models.CharField(max_length=220)
#     created_date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name

#
# class Drop(models.Model):
#     name = models.CharField(max_length=120, unique=True)
#     created_date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name