from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from shipping.models import UserPickUpStation
from accounts.decorators import required_access
from accounts.models import Customer
from utils.utils import generate_key
# from .filter import OrderFilter
from orders.models import Order, OrderItem
from shipping.models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

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

class DeliveryListView(ListView):
    # model = Delivery
    template_name = 'store/delivery-list.html'
    context_object_name = 'delivery'


def invoice(request):
    return render(request, 'store/invoice.html')

class ProductView(View):
    def get(self, request):
        products = Product.objects.filter(in_stock = True)
        context = {'products': products}
        return render(request, 'store/view-products.html', context)


def product_detail(request, name):
    product = get_object_or_404(Product, slug=name)
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
            return redirect('store:category_list')
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

    

 # cart functions

# @login_required
def add_to_cart(request, pk):
    quantity = request.GET.get('quantity', 1)
    product = get_object_or_404(Product, pk=pk)

    # Check if requested quantity is in stock
    if product.quantity < int(quantity):
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('store:view-product')

    # Check if the total quantity in the order exceeds the available stock
    order_items = OrderItem.objects.filter(product=product, order__is_completed=False, order__user=request.user)
    total_quantity_in_order = sum(order_item.quantity for order_item in order_items)
    if product.quantity < total_quantity_in_order + int(quantity):
        messages.error(request, f"Only {product.quantity } {product.name} available in stock.")
        return redirect('store:view-product')

    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += int(quantity)
    order_item.save()
    messages.success(request, 'Item added to cart.', extra_tags='text-success')
    return redirect('store:view-product')


# @login_required
def view_cart(request):
    user = User.objects.all()
    
    # Retrieve the latest pending order if one exists, otherwise create a new one
    try:
        order = Order.objects.filter(user=request.user, is_completed=False).latest('id')
    except Order.DoesNotExist:
        order = Order.objects.create(user=request.user)

    order_items = order.orderitem_set.all()

    if request.method == 'POST':
        if 'order_item_id' in request.POST:
            # Handle updates to order items
            order_item_id = int(request.POST.get('order_item_id'))
            order_item = OrderItem.objects.get(id=order_item_id, order=order)

            if 'increment' in request.POST:
                order_item.quantity += 1
                order_item.save()
                messages.success(request, 'Quantity updated successfully.', extra_tags='text-success')

            if 'decrement' in request.POST:
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.success(request, 'Quantity updated successfully.', extra_tags='text-success')
                else:
                    order_item.delete()
                    messages.success(request, 'Item removed from order.', extra_tags='text-success')

        elif 'pickup_station_id' in request.POST:
            # Handle selection of a pickup station by the user
            pickup_station_id = int(request.POST.get('pickup_station_id'))
            pickup_station = UserPickUpStation.objects.get(id=pickup_station_id)
            shipping = Shipping.objects.create(order=order, station=pickup_station)
            messages.success(request, 'Pickup station selected successfully.', extra_tags='text-success')

    # Calculate the subtotal for each order item and save it
    for item in order_items:
        item.subtotal = item.product.price * item.quantity
        item.save()

    # Calculate the order total by summing the subtotals of each order item
    order_total = sum([item.subtotal for item in order_items])

    # Get the available pickup stations
    userpickupstations = UserPickUpStation.objects.all()

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
        'userpickupstations': userpickupstations
    }
    return render(request, 'store/cart.html', context)
