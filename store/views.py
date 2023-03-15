from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages

from accounts.decorators import required_access
from accounts.models import Customer
from utils.utils import generate_key
# from .filter import OrderFilter
from orders.models import Order
from .forms import *
from django.shortcuts import get_object_or_404, render


from .models import (
    Product,Category
)


# from .forms import (
#     ProductForm,
#     OrderForm,
#     DeliveryForm
# )


# Create your views here.
# dashboard views
@required_access(login_url=reverse_lazy('accounts:login'), user_type="SM")
def SM_dashboard(request):
    return render(request, 'dashboard/inventorymanager-dashboard.html')


# class CustomerListView(ListView):
#     model = Customer
#     template_name = 'store/customer-list.html'
#     context_object_name = 'customer'


# #Product views
# def create_product(request):
#     forms = ProductForm()
#     if request.method == 'POST':
#         forms = ProductForm(request.POST, request.FILES)
#         if forms.is_valid():
#             forms.save()
#             return redirect('store:product-list')
#     context = {
#         'form': forms
#     }
#     return render(request, 'store/add-product.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product-list.html'
    context_object_name = 'product'

class OrderListView(ListView):
    # model = Order
    template_name = 'store/order-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['order'] = Order.objects.all().order_by('-id')
        return context


# # Delivery views
# @login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create-delivery.html', context)


class DeliveryListView(ListView):
    # model = Delivery
    template_name = 'store/delivery-list.html'
    context_object_name = 'delivery'


def invoice(request):
    return render(request, 'store/invoice.html')


def view_product(request):
    products = Product.objects.all()
    return render(request, 'store/view-products.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock = True)
    return render(request, 'store/product-detail.html',{'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug= category_slug)
    products = Product.objects.filter(category = category)
    return render(request,'store/category.html',{'category':category,'product': products})

def product(request):
    product = Product.objects.all()
    return render(request, 'store/products.html', {'product': product})

def categories(request):
    return{
        'categories':Category.objects.all()
    }


def productlistAjax(request):
    products= Product.objects.filter(is_active=True).values_list('name', flat=True)
    productsList = list(products)

    return JsonResponse(productsList, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
             return redirect(request.META.get('HTTP_REFRER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                return redirect('product_detail/'+product.slug)
            else:
                messages.info(request,"No matched product")
                return redirect(request.META.get('HTTP_REFRER'))

    return redirect(request.META.get('HTTP_REFRER'))

# create product by inventory manager
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully")
            return redirect('store:product-list')
        else:
            messages.warning(request, "Error creating Product")
    context = {'form': form}
    return render(request, 'store/add-product.html', context)


# update product by inventory manager
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully")
            return redirect('store:product-list')
        else:
            messages.warning(request, "Error updating Product")
    context = {'form': form}
    return render(request, 'store/add-product.html', context)

# delete product
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store:product-list')
        messages.success(request, "Product deleted successfully")

    context = {"product":product}
    return render(request, 'store/delete-product.html', context)

# create category by inventory manager
def create_category(request):
    form  = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully")
            return redirect('store:product-list')
        else:
            messages.warning(request, "Error creating Category")
    context = {'form': form}
    return render(request, 'store/add-category.html', context)

# update category
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully")
            return redirect('store:category_list')
        else:
            messages.warning(request, "Error updating Product")
    context = {'form': form}
    return render(request, 'store/add-category.html', context)


# delete category
def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('store:category_list')
    context = {"category":category}
    return render(request, 'store/delete-category.html', context)

def category_list(request):
    category = Category.objects.filter()
    context = {"category":category}
    return render(request, "store/category-list.html", context)