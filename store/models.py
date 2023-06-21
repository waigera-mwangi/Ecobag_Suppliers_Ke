from django.db import models
# from pkg_resources import _
from django.urls import reverse
# from moneyfield import MoneyField
from djmoney.models.fields import MoneyField
# from moneyed import Money
from accounts.models import User, Customer

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    # def get_absolute_url(self):
    #     return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'product', on_delete=models.CASCADE,null = True,default='Gift_bag')
    name = models.CharField(max_length=120, unique=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='KES', verbose_name='Price' )
    quantity = models.IntegerField()
    image = models.ImageField()
    created_date = models.DateField(auto_now_add=True)
    updated = models.DateField(('Updated'), auto_now=True)
    description = models.CharField(max_length=100)
    in_stock = models.BooleanField(default = True)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.name