from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from accounts.decorators import required_access
from accounts.models import Customer
from utils.utils import generate_key
from .filter import OrderFilter
from .forms import ProductForm, DeliveryForm, OrderForm, OrderPaymentForm
from django.shortcuts import get_object_or_404, render


from .models import (
    # Product,
    Order, Product, Delivery, OrderItem,Category
)


# from .forms import (
#     ProductForm,
#     OrderForm,
#     DeliveryForm
# )


# Create your views here.
# dashboard views
@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="SM")
def SM_dashboard(request):
    return render(request, 'dashboard/inventorymanager-dashboard.html')


# class CustomerListView(ListView):
#     model = Customer
#     template_name = 'store/customer-list.html'
#     context_object_name = 'customer'


# #Product views
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('store:product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/add-product.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product-list.html'
    context_object_name = 'product'


# Order views
# @login_required(login_url='login')
# def create_order(request):
#     forms = OrderForm()
#     if request.method == 'POST':
#         forms = OrderForm(request.POST)
#         if forms.is_valid():
#             supplier = forms.cleaned_data['supplier']
#             product = forms.cleaned_data['product']
#             design = forms.cleaned_data['design']
#             color = forms.cleaned_data['color']
#             buyer = forms.cleaned_data['buyer']
#             season = forms.cleaned_data['season']
#             drop = forms.cleaned_data['drop']
#             Order.objects.create(
#                 customer=customer,
#                 product=product,
#                 design=design,
#                 color=color,
#                 status='pending'
#             )
#             return redirect('order-list')
#     context = {
#         'form': forms
#     }
#     return render(request, 'store/create_order.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
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
    model = Delivery
    template_name = 'store/delivery-list.html'
    context_object_name = 'delivery'


def invoice(request):
    return render(request, 'store/invoice.html')


def view_product(request):
    products = Product.objects.all()
    return render(request, 'store/view-products.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product-detail.html',{'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug= category_slug)
    products = Product.objects.filter(category = category)
    return render(request,'store/category.html',{'category':category,'product': products})

def product(request):
    product = Product.objects.all()
    return render(request, 'store/products.html', {'product': product})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    # orders = customer.order_set.all()
    orders = Order.objects.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'store/customer.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'store/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'store/delete.html', context)


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'dashboard/salesmanager-dashboard.html', context)


def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'store/user.html', context)


def add_to_cart(request):
    data = {}
    customer = request.user.UserTypes.CUSTOMER,
    product = Product.objects.filter().first()
    if Order.objects.filter(customer=customer, is_active=True, delivered=False).exists():
        order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
        if OrderItem.objects.filter(order=order, product=product).exists():
            order_item = OrderItem.objects.get(order=order, product=product)
            quantity = order_item.quantity + 1
            if quantity <= product.quantity:
                order_item.quantity = quantity
                order_item.save()
                data['message'] = f"{quantity} {product.name} has been added to cart"
            else:
                data['info'] = f"{quantity} {product.name} are not available we only have {product.quantity} remaining."
        else:
            if product.quantity >= 1:
                OrderItem.objects.create(order=order, product=product, quantity=1)
                data['message'] = f"1 {product.name} has been added to cart"
            else:
                data['info'] = f"Sorry this item is out of stock"
    else:
        order = Order.objects.create(customer=customer, is_active=True, completed=False,
                                     transaction_id=generate_key(6, 6))
        if product.quantity >= 1:
            OrderItem.objects.create(order=order, product=product, quantity=1)
            data['message'] = f"1 {product.name} has been added to cart"
        else:
            data['info'] = f"Sorry this item is out of stock"
    return JsonResponse(data)


def cart_list(request):
    data = {}
    order = Order.objects.filter(customer=request.user.customer, is_active=True, delivered=False).first()
    try:
        data['object_list'] = order.orderitem_set.all()
    except AttributeError:
        pass
    data['order'] = order
    return render(request, 'store/cart.html', data)


def remove_from_cart(request, slug):
    data = {}
    customer = request.user.customer
    product = Product.objects.filter(slug=slug).first()
    order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    item = OrderItem.objects.filter(order=order, product=product).first()
    item.delete()
    data['message'] = f"{product.name} has been removed from cart successfully"
    return JsonResponse(data)


def decrease_quantity(request, slug):
    data = {}
    customer = request.user.customer
    product = Product.objects.filter(slug=slug).first()
    order = Order.objects.filter(customer=customer, is_active=True, delivered=False).first()
    item = OrderItem.objects.filter(order=order, product=product).first()
    quantity = item.quantity - 1
    if quantity >= 1:
        item.quantity = quantity
        item.save()
        data['message'] = f"{product.name} quantity has been decreased to {quantity}"
    else:
        item.delete()
        data['message'] = f"{product.name} has been removed from cart successfully."
    return JsonResponse(data)


def increase_quantity(request, slug):
    data = {}
    customer = request.user.customer
    product = Product.objects.filter(slug=slug).first()
    order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    item = OrderItem.objects.filter(order=order, product=product).first()
    quantity = item.quantity + 1
    if product.quantity >= quantity:
        item.quantity = quantity
        item.save()
        data['message'] = f"{product.name} quantity has been increased to {quantity}"
    else:
        data['info'] = f"{quantity} {product.name} are not available we only have {product.quantity} remaining."
    return JsonResponse(data)


def clear_cart(request):
    data = {}
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    order.is_active = False
    order.save()
    data['message'] = "Cart has been cleared successfully."
    return JsonResponse(data)


def checkout(request):
    data = {}
    try:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
        data['order'] = order
        data['form'] = OrderPaymentForm
        data['object_list'] = order.orderitem_set.all()
        products = []
        for item in order.orderitem_set.all():
            product = {
                'quantity': item.quantity,
                'name': item.product.name,
                'slug': item.product.slug,
            }
            products.append(product)
        print(products)
        for item in products:
            product = Product.objects.filter(slug=item['slug']).first()
            if product.quantity >= item['quantity']:
                print(f"{product.quantity} >= {item['quantity']}")
                print("Everything is fine products exists")
            else:
                instance = OrderItem.objects.get(order=order, product=product)
                if product.quantity > 0:
                    instance.quantity = product.quantity
                    instance.save()
                else:
                    instance.delete()
    except AttributeError:
        pass
    return render(request, 'store/checkout.html', data)


def checkout_pay(request):
    data = {}
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    if request.method == "POST":
        form = OrderPaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            mpesa = instance.mpesa
            if len(mpesa) == 10:
                if instance.amount == order.get_cart_total:
                    instance.order = order
                    instance.transaction_id = generate_key(8, 8)
                    instance.save()
                    data['message'] = "Payment has been done successfully"
                    order.completed = True
                    order.save()
                    items = order.orderitem_set.all()
                    for item in items:
                        product = Product.objects.filter(id=item.product.id).first()
                        quantity = product.quantity - item.quantity
                        product.quantity = quantity
                        product.save()
                else:
                    data['info'] = f"amount sent is {instance.amount} but amount required is {order.get_cart_total}"
            else:
                data['mpesa'] = "Enter valid mpesa code"
        else:
            data['info'] = "This form is invalid"
            data['form'] = form.errors
    return JsonResponse(data)


def order_list(request):
    data = {}
    customer = request.user.customer
    order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    data['order'] = order
    return render(request, 'store/checkout.html', data)

def categories(request):
    return{
        'categories':Category.objects.all()
    }
