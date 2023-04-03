# import form as form
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from accounts.decorators import required_access
from accounts.forms import *
from accounts.models import User, CustomerProfile, Profile
from django.urls import reverse_lazy
from .models import *
from orders.models import Order
from store.models import *
from supply.models import *
from brands.models import *
from delivery.models import *
from . import context_processors
# from orders.views import user_orders



class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/customer-registration.html"
    form_class = CustomerSignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('accounts:login')


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, "You've logged out successfully.")
        return redirect('/')


def loginView(request):
    loginform = LoginForm(request.POST or None)
    msg = ''

    if request.method == 'POST':
        if loginform.is_valid():
            username = loginform.cleaned_data.get('username')
            password = loginform.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.user_type == "FM":
                login(request, user)
                return redirect('accounts:finance-manager')
                
            elif user is not None and user.user_type == "SM":
                login(request, user)
                return redirect('accounts:inventory')

            elif user is not None and user.user_type == "CM":
                login(request, user)
                return redirect('accounts:customer')

            elif user is not None and user.user_type == "DR":
                login(request, user)
                return redirect('accounts:driver')
            
            elif user is not None and user.user_type == "RD":
                login(request, user)
                return redirect('accounts:supplier')

            elif user is not None and user.user_type == "MN":
                login(request, user)
                return redirect('accounts:manager')

            elif user is not None and user.user_type == "BR":
                login(request, user)
                return redirect('accounts:brander')

            elif user is not None and user.user_type == "DM":
                login(request, user)
                return redirect('accounts:dispatch-manager')

            else:
                msg = 'Invalid login credentials'
        else:
            msg = 'error validating form'
    return render(request, 'accounts/user-login.html', {'form': loginform, 'msg': msg})


@required_access(login_url=reverse_lazy('accounts:login'), user_type="CM")
def customer(request):
    return redirect('store:view-product')



required_access(login_url=reverse_lazy('accounts:login'), user_type="SM")
def inventory(request):
    pending_cart_count = Order.objects.filter(payment__payment_status='Pending').count()
    completed_cart_count = Order.objects.filter(payment__payment_status='Approved').count()
    products = Product.objects.all()
    total_products = products.count()
    inStock = products.filter(in_stock=True)
    total_inStock = inStock.count()
    category  = Category.objects.all()
    total_categories = category.count()
    context = {
        'pending_cart_count': pending_cart_count,
        'completed_cart_count': completed_cart_count,
        'products':products,
        'total_products':total_products,
        'total_categories':total_categories,
        'total_inStock':total_inStock,
        
    }
    return render(request, 'inventory/index.html', context)



@required_access(login_url=reverse_lazy('accounts:login'), user_type="FM")
def finance_manager(request):
    orders = Order.objects.all()
    total_orders = orders.count()
   
    
    context = {'orders':orders,
              'total_orders':total_orders,
    }

    return render(request, 'finance-manager.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="DR")
def driver(request):
    deliveries = Delivery.objects.all().count()
    orders = Order.objects.all()
    # approved = orders.filter(orderstatus='Approved').count()
    context = {
               'deliveries':deliveries,
    }
    return render(request, 'driver.html', context)

@required_access(login_url=reverse_lazy('accounts:login'), user_type="RD")
def supplier(request):
    user = request.user
    all_tenders_count = SupplyTender.objects.count()
    pending_tenders_count = SupplyTender.objects.filter(tender_status='Pending', user=user).count()
    complete_tenders_count = SupplyTender.objects.filter(tender_status='Complete', user=user).count()
    context = {
        'all_tenders_count': all_tenders_count,
        'pending_tenders_count': pending_tenders_count,
        'complete_tenders_count': complete_tenders_count,
    }
    return render(request, 'supplier/index.html', context=context)





@required_access(login_url=reverse_lazy('accounts:login'), user_type="MN")
def manager(request):
    return render(request, 'manager.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="BR")
def brander(request):
    brands = Brand.objects.all()
    total_brands = brands.count()
    context = {'total_brands':total_brands}
    return render(request, 'brander.html', context)

@required_access(login_url=reverse_lazy('accounts:login'), user_type="DM")
def dispatch_manager(request):
    orders = Order.objects.all()
    
    deliveries = Delivery.objects.all().count()
    context = {
               'deliveries':deliveries,

    }
    return render(request, 'dispatch-manager.html', context)


#Change password
def password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/change-password.html', {'form': form})


#profile settings
# def profile_main(request):
#     p_form = FinanceProfileForm(instance=request.user.finance.financeprofile)
#     form = FinanceForm(instance=request.user.finance)
#     if request.method == "POST":
#         p_form = FinanceProfileForm(request.POST, request.FILES, instance=request.user.finance.financeprofile)
#         form = FinanceForm(request.POST, instance=request.user.finance)
#         if form.is_valid() and p_form.is_valid():
#             form.save()
#             p_form.save()
#             messages.success(request, "Your Profile has been updated!")
#     context = {
#         'p_form': p_form,
#         'form': form,
#     }
#     return render(request, 'finance/forms/profile.html', context)


# def profile(request):
#     # profile = Profile.object.all()
#     profile = Profile.objects.get_or_create(user=request.user)
#     p_form = CustomerProfileForm(instance=profile)
#     form = CustomerForm(instance=request.user)
#     if request.method == "POST":
#         p_form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
#         form = CustomerForm(request.POST, instance=request.user)
#         p_form.save()
#         form.save()
#         messages.success(request, 'Profile updated successfully')
#     # order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
#     context = {+
#         'p_form': p_form,
#         'form': form,
#         # 'order': order
#     }
#     return render(request, 'accounts/profile.html',  context)


class FAQQuestionTypeListView(ListView):
    template_name = 'faq/customer_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class D_FAQ(ListView):
    template_name = 'faq/driver_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class S_FAQ(ListView):
    template_name = 'faq/supplier_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class B_FAQ(ListView):
    template_name = 'faq/brander_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class I_FAQ(ListView):
    template_name = 'faq/inventory_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class DP_FAQ(ListView):
    template_name = 'faq/dispatch_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'

class F_FAQ(ListView):
    template_name = 'faq/finance_faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'


# profiles
def customer_profile(request):
    
    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no customer profile exists for the user
        customer_profile = CustomerProfile.objects.create(user=request.user)

    # customer_profile = CustomerProfile.objects.get(user=request.user)
    # profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    p_form = CustomerProfileForm(instance=customer_profile)
    form = CustomerForm(instance=request.user)

    # Retrieve profile image URL

    if request.method == "POST":
        p_form = CustomerProfileForm(request.POST, request.FILES, instance=customer_profile)
        form = CustomerForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'customer_profile': customer_profile,
    }
    return render(request, 'accounts/profiles/customer-profile-create.html',  context)


def finance_profile(request):
  
    try:
        finance_profile = FinanceProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        finance_profile = FinanceProfile.objects.create(user=request.user)

    p_form = FinanceProfileForm(instance=finance_profile)
    form = FinanceForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = finance_profile.image.url if finance_profile.image else None

    if request.method == "POST":
        p_form = FinanceProfileForm(request.POST, request.FILES, instance=finance_profile)
        form = FinanceForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'finance_profile': finance_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/finance-profile.html',  context)


def brander_profile(request):
  
    try:
        brander_profile = BranderProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        brander_profile = BranderProfile.objects.create(user=request.user)

    p_form = BranderProfileForm(instance=brander_profile)
    form = BranderForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = brander_profile.image.url if brander_profile.image else None

    if request.method == "POST":
        p_form = BranderProfileForm(request.POST, request.FILES, instance=brander_profile)
        form = BranderForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'brander_profile': brander_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/brander-profile.html',  context)

def dispatch_profile(request):
  
    try:
        dispatch_profile = DispatchProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        dispatch_profile = DispatchProfile.objects.create(user=request.user)

    p_form  = DispatchProfileForm(instance=dispatch_profile)
    form = DispatchForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = dispatch_profile.image.url if dispatch_profile.image else None

    if request.method == "POST":
        p_form = DispatchProfileForm(request.POST, request.FILES, instance=dispatch_profile)
        form = DispatchForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'dispatch_profile': dispatch_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/dispatch-profile.html',  context)

def driver_profile(request):

    try:
        driver_profile = DispatchProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        driver_profile = DispatchProfile.objects.create(user=request.user)

    p_form = DriverProfileForm(instance=driver_profile)
    form = DriverForm(instance=request.user)

    # Retrieve profile image URL
    

    if request.method == "POST":
        p_form = DriverProfileForm(request.POST, request.FILES, instance=driver_profile)
        form = DriverForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
    context = {
        'p_form': p_form,
        'form': form,
        'driver_profile': driver_profile,
        
    }
    return render(request, 'accounts/profiles/driver-profile.html',  context)

def inventory_profile(request):
    try:
        inventory_profile = InventoryProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        inventory_profile = InventoryProfile.objects.create(user=request.user)

    p_form = InventoryProfileForm(instance=inventory_profile)
    form = InventoryForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = inventory_profile.image.url if inventory_profile.image else None

    if request.method == "POST":
        p_form = InventoryProfileForm(request.POST, request.FILES, instance=inventory_profile)
        form = InventoryForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
            # Update profile image URL after saving
            profile_image_url = inventory_profile.image.url if inventory_profile.image else None
    context = {
        'p_form': p_form,
        'form': form,
        'inventory_profile': inventory_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/inventory-profile.html',  context)



def supplier_profile(request):
    try:
        supply_profile = SupplyProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        supply_profile = SupplyProfile.objects.create(user=request.user)

    p_form = SupplierProfileForm(instance=supply_profile)
    form = SupplierForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = supply_profile.image.url if supply_profile.image else None

    if request.method == "POST":
        p_form = SupplierProfileForm(request.POST, request.FILES, instance=supply_profile)
        form = SupplierForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
            # Update profile image URL after saving
            profile_image_url = supply_profile.image.url if supply_profile.image else None
    context = {
        'p_form': p_form,
        'form': form,
        'supply_profile': supply_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/supplier-profile.html',  context)

# change password

def customer_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/customer-change-password.html', {'form': form})


def driver_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/driver-change-password.html', {'form': form})


def supplier_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/supplier-change-password.html', {'form': form})


def finance_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/finance-change-password.html', {'form': form})


def inventory_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/inventory-change-password.html', {'form': form})


def dispatch_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/dispatch-change-password.html', {'form': form})

def brander_password_change(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.info(request, 'Please correct the errors below.')
    return render(request, 'accounts/password-change/brander-change-password.html', {'form': form})

