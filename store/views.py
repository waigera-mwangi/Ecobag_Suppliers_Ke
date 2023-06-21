from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from accounts.decorators import required_access
from accounts.models import User
from django.db.models import Sum
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from utils.utils import generate_key
# from .filter import OrderFilter
from orders.models import *
from finance.models import *
from shipping.models import *
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

from .models import (
    Product,Category
)

from django.db.models import F, Sum


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

#  view products in category
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})


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
            return redirect('store:inventory_category_list')
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
            messages.success(request, "Category updated successfully")
            return redirect('store:inventory_category_list')
        else:
            messages.warning(request, "Error updating Category")
    context = {'form': form}
    return render(request, 'inventory/includes/add-category.html', context)



def inventory_category_list(request):
    category = Category.objects.filter()
    context = {"category":category}
    return render(request, "store/category-list.html", context)

    # view products by category
class ProductByCategoryView(ListView):
    model = Product
    template_name = 'store/product_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        return Product.objects.filter(category=category)

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

    # Calculate the subtotal for each order item and save it
    for item in order_items:
        item.subtotal = item.product.price * item.quantity
        item.save()

    # Calculate the order total by summing the subtotals of each order item
    order_total = sum([item.subtotal for item in order_items])

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'store/cart.html', context)


from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.contrib import messages
from accounts.decorators import required_access
from accounts.models import Customer
from utils.utils import generate_key
from orders.models import Order, OrderItem
from .forms import *
from .models import Product, Category
from django.shortcuts import render
from .models import Category

def index(request):
    categories = Category.objects.all()
    # your code here
    return render(request, 'index.html', {'categories': categories})



# dashboard views
@required_access(login_url=reverse_lazy('accounts:login'), user_type="SM")
def SM_dashboard(request):
    return render(request, 'dashboard/inventorymanager-dashboard.html')


class ProductListView(ListView):
    model = Product
    template_name = 'store/product-list.html'
    context_object_name = 'product'


class OrderListView(ListView):
    template_name = 'store/order-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeliveryListView(ListView):
    template_name = 'store/delivery-list.html'
    context_object_name = 'delivery'


def invoice(request):
    return render(request, 'store/invoice.html')


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {'products': products}
        return render(request, 'store/view-products.html', context)


def product_detail(request, name):
    product = get_object_or_404(Product, slug=name, in_stock=True)
    return render(request, 'store/product-detail.html', {'product': product})


def product(request):
    product = Product.objects.all()
    return render(request, 'store/products.html', {'product': product})


def productlistAjax(request):
    products = Product.objects.filter(is_active=True).values_list('name', flat=True)
    productsList = list(products)

    return JsonResponse(productsList, safe=False)


def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                return redirect('product_detail/' + product.slug)
            else:
                messages.info(request, "No matched product")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


 # optimized
# @login_required
def customer_order_list(request):
        user = request.user
        orders = Order.objects.filter(user=user, is_completed=True)
        order_list = []
        for order in orders:
            payment = Payment.objects.filter(order=order).first()
            if payment:
                order_info = {
                    'transaction_id': payment.transaction_id,
                    'username': order.user.username,
                    'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                    # 'total_cost': order.subtotal,
                    'payment_status': payment.payment_status,
                    'date_ordered': order.date_ordered,
                    'order_id': order.id,  # Add cart_id to the dictionary
                }
                order_list.append(order_info)
        return render(request, 'store/customer_order_list.html', {'order_list': order_list})    


# @login_required
def customer_order_detail(request, order_id):
    user = request.user
    order = get_object_or_404(Order, user=user, id=order_id, is_completed=True)
    payment = Payment.objects.filter(order=order).first()
    order_items = order.orderitem_set.all()
    order_total = order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost']



    context = {
        'order': order,
        'payment': payment,
        'order_items': order_items,
        'order_total' : order_total, 
    }
    return render(request, 'store/customer_order_detail.html', context)

# @login_required
def customer_order_invoice(request):
        user = request.user
        orders = Order.objects.filter(user=user, is_completed=True)
        order_list = []
        for order in orders:
            payment = Payment.objects.filter(order=order).first()
            if payment:
                order_info = {
                    'transaction_id': payment.transaction_id,
                    'username': order.user.username,
                    'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                    'order_total' : order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                    'payment_status': payment.payment_status,
                    'date_ordered': order.date_ordered,
                    'order_id': order.id,  # Add cart_id to the dictionary
                }
                order_list.append(order_info)
        return render(request, 'finance/customer-invoice.html', {'order_list': order_list})  

def customer_order_pdf(request, order_id):
    user = request.user
    order = get_object_or_404(Order, user=user, id=order_id, is_completed=True)
    payment = Payment.objects.filter(order=order).first()
    order_items = order.orderitem_set.all()
    order_total = order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost']
    
    # Load template for receipt
    template = get_template('finance/order_payment_receipt.html')
    context = {
        'order': order,
        'payment': payment,
        'order_items': order_items,
        'order_total': order_total,
        'user': user,
    }
    html = template.render(context)

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), buffer)

    if not pdf.err:
        # Get the value of the BytesIO buffer and write it to the response
        pdf_value = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="order_invoice_{}.pdf"'.format(order_id)
        response.write(pdf_value)
        return response

    return HttpResponse('Error generating PDF!')

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

                    
    # Calculate the subtotal for each order item and save it
    for item in order_items:
        item.subtotal = item.product.price * item.quantity
        item.save()

    # Calculate the order total by summing the subtotals of each order item
    order_total = sum([item.subtotal for item in order_items])

    context = {
        'order': order,
        'order_items': order_items,
        'order_total': order_total,
    }
    return render(request, 'store/cart.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import DetailView



# class CategoryListView(LoginRequiredMixin, ListView):
#     model = Category
#     template_name = 'inventory/includes/category_list.html'
#     context_object_name = 'categories'

# class CategoryCreateView(LoginRequiredMixin,  CreateView):
#     model = Category
#     template_name = 'inventory/includes/create_category.html'
#     form_class = CategoryForm
#     success_url = reverse_lazy('inventory:category-list')


#     def test_func(self):
#         return self.request.user.is_superuser

# class CategoryUpdateView(LoginRequiredMixin,  UpdateView):
#     model = Category
#     template_name = 'inventory/includes/category_update_form.html'
#     form_class = CategoryForm

#     def test_func(self):
#         return self.request.user.is_superuser

# class CategoryDeleteView(LoginRequiredMixin, DeleteView):
#     model = Category
#     template_name = 'category_confirm_delete.html'
#     success_url = reverse_lazy('inventory:category-list')


# def Category(request):
#     category = Category.objects.all()
#     return render (request,  {'category': category})

#     def test_func(self):
#         return self.request.user.is_superuser

class ProductListView(ListView):
    model = Product
    template_name = 'inventory/includes/product_list.html'
    context_object_name = 'products'

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from .models import Product

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'inventory/includes/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('store:product-list')

    def form_valid(self, form):
        # Set the user of the product to the currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add error messages to the form if it is invalid
        messages.error(self.request, 'An error occurred. Please try again.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        # Set the user of the product to the currently logged in user
        request.POST = request.POST.copy()
        request.POST['user'] = request.user.id
        return super().post(request, *args, **kwargs)


  

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'inventory/includes/product_update_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('store:product-list')

    def test_func(self):
        return self.request.user.is_superuser

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/includes/product_confirm_delete.html'
    success_url = reverse_lazy('store:product-list')

    def test_func(self):
        return self.request.user.is_superuser


class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/includes/product_detail.html'
    context_object_name = 'product'


class ProductDetailViewCustomer(DetailView):
    model = Product
    template_name = 'inventory/includes/product_detail_customer.html'
    context_object_name = 'product'


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'inventory/includes/product_detail_view.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        return context





# views.py
class OrderListView(ListView):
    model = Order
    template_name = 'inventory/order_list.html'
    context_object_name = 'carts'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('inventory:order-list')
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'order successfully deleted.')
        return super().delete(request, *args, **kwargs)





class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order-list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Order deleted successfully.")
        return super().delete(request, *args, **kwargs)


def approve_payment(request, transaction_id):
    payment = Payment.objects.get(transaction_id=transaction_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'approve':
            payment.payment_status = 'Approved'
            order = Order.objects.get(payment=payment)
            order.is_completed = True
            order.save()
        elif status == 'reject':
            payment.payment_status = 'Rejected'
        payment.save()  # save the payment status change
        return redirect('store:order-payment')

    context = {
        'payment': payment,
    }
    return render(request, 'finance/order-payment.html', context)

def order_rejected_payment(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        payment = Payment.objects.filter(order=order, payment_status='Rejected').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                'order_total' : order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                'payment_status': payment.payment_status,
                'date_ordered': order.date_ordered,
                'payment_id': payment.id,  # add payment_id to order_info
            }
            order_list.append(order_info)
    return render(request, 'finance/order-payment-rejected.html', {'order_list': order_list})

def order_approved_payment(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        payment = Payment.objects.filter(order=order, payment_status='Approved').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                'order_total' : order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                'payment_status': payment.payment_status,
                'date_ordered': order.date_ordered,
                'payment_id': payment.id,  # add payment_id to order_info
            }
            order_list.append(order_info)
    return render(request, 'finance/order_approved_payment.html', {'order_list': order_list})

def order_payment(request):
    orders = Order.objects.filter(is_completed=True)
    order_list = []
    for order in orders:
        payment = Payment.objects.filter(order=order, payment_status='pending').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                'order_total' : order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                'payment_status': payment.payment_status,
                'date_ordered': order.date_ordered,
                'payment_id': payment.id,  # add payment_id to order_info
            }
            order_list.append(order_info)
    return render(request, 'finance/order-payment.html', {'order_list': order_list})


User = get_user_model()

def assign_driver_order_list(request):
    orders = Order.objects.filter(is_completed=True, shipping__isnull=True)
    order_list = []
    for order in orders:
        payment = Payment.objects.filter(order=order, payment_status='Approved').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'payment_status': payment.payment_status,
                'county': payment.county,
                'town': payment.town,
                'phone_number': payment.phone_number,
                'date_ordered': order.date_ordered,
                'payment_id': payment.id,
                'id': order.id,
                'driver': None,
               
            }
            shipping = Shipping.objects.filter(order=order).first()
            if shipping:
                order_info['driver'] = shipping.driver
            order_list.append(order_info)

    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        driver_id = request.POST.get('driver_id', None)
        if order_id and driver_id:
            try:
                order = Order.objects.get(pk=order_id)
                if Shipping.objects.filter(order=order).exists():
                    messages.error(request, f"Order has already been assigned to a driver")
                else:
                    driver = User.objects.filter(pk=driver_id, user_type=User.UserTypes.DRIVER).first()
                    shipping = Shipping.objects.create(order=order, driver=driver)
                    messages.success(request, f"Order has been assigned to {driver}")
            except (Order.DoesNotExist, User.DoesNotExist):
                messages.error(request, "Failed to assign driver")
        else:
            messages.error(request, "Missing order_id or driver_id")

        return redirect('store:assign-order-list')


    drivers = User.objects.filter(user_type=User.UserTypes.DRIVER)
    return render(request, 'dispatch/assign_order_list.html', {'order_list': order_list, 'drivers': drivers})



def assigned_order_list(request):
    orders = Order.objects.filter(is_completed=True, shipping__isnull=False)
    order_list = []
    for order in orders:
        payment = Payment.objects.filter(order=order, payment_status='Approved').first()
        if payment:
            order_info = {
                'transaction_id': payment.transaction_id,
                'username': order.user.username,
                'quantity': order.products.aggregate(Sum('orderitem__quantity'))['orderitem__quantity__sum'],
                'order_total' : order.products.annotate(item_total=F('orderitem__quantity') * F('price')).aggregate(total_cost=Sum('item_total'))['total_cost'],
                'payment_status': payment.payment_status,
                'county':payment.county,
                'town':payment.town,
                'phone_number':order.user.phone_number,
                'date_ordered': order.date_ordered,
                'payment_id': payment.id,
                'id': order.id,
                'driver': None,
               
            }
            shipping = Shipping.objects.filter(order=order).first()
            if shipping:
                order_info['driver'] = shipping.driver
            order_list.append(order_info)

    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        driver_id = request.POST.get('driver_id', None)
        if order_id and driver_id:
            try:
                order = Order.objects.get(pk=order_id)
                if Shipping.objects.filter(order=order).exists():
                    messages.error(request, f"{order} has already  assigned to a driver")
                else:
                    driver = User.objects.filter(pk=driver_id, user_type=User.UserTypes.DRIVER).first()
                    shipping = Shipping.objects.create(order=order, driver=driver)
                    messages.success(request, f"{order} has been assigned to {driver}")
            except (Order.DoesNotExist, User.DoesNotExist):
                messages.error(request, "Failed to assign driver")
        else:
            messages.error(request, "Missing order_id or driver_id")

        return redirect('inventory:assigned-order-list')


    drivers = User.objects.filter(user_type=User.UserTypes.DRIVER)
    return render(request, 'dispatch/assigned_order_list.html', {'order_list': order_list, 'drivers': drivers})

