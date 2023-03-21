# import form as form
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from accounts.decorators import required_access
from accounts.forms import *
from accounts.models import User, CustomerProfile, Profile
from django.urls import reverse_lazy

from orders.models import Order
from store.models import *
from supply.models import *
from brands.models import *
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
                return redirect('accounts:inventory-manager')

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

@required_access(login_url=reverse_lazy('accounts:login'), user_type="SM")
def inventory_manager(request):
    products = Product.objects.all()
    total_products = products.count()
    inStock = products.filter(in_stock=True)
    isActive = products.filter(is_active=True)
    total_isActive = isActive.count()
    total_inStock = inStock.count()
    category  = Category.objects.all()
    total_categories = category.count()

    context = {'products':products,
               'total_products':total_products,
               'total_categories':total_categories,
               'total_inStock':total_inStock,
               'total_isActive':total_isActive,
    }


    return render(request, 'inventory-manager.html',context)


@required_access(login_url=reverse_lazy('accounts:login'), user_type="FM")
def finance_manager(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    pending = orders.filter(orderstatus='Pending').count()
    approved = orders.filter(orderstatus='Approved').count()
    rejected = orders.filter(orderstatus='Rejected').count()
    out_for_shipping = orders.filter(orderstatus='Out for shipping').count()
    completed = orders.filter(orderstatus='Completed').count()

    context = {'orders':orders,
              'total_orders':total_orders,
              'pending':pending,
              'approved':approved,
              'rejected':rejected,
              'out_for_shipping':out_for_shipping,
              'completed':completed}
    
    return render(request, 'finance-manager.html', context)

@required_access(login_url=reverse_lazy('accounts:login'), user_type="DR")
def driver(request):
    return render(request, 'driver.html')

@required_access(login_url=reverse_lazy('accounts:login'), user_type="RD")
def supplier(request):
    supply_requests = SupplyTender.objects.all()
    total_requests = supply_requests.count()
    supplies = ProductSupply.objects.all()
    total_supplies = supplies.count()
    context = {'total_requests':total_requests,
               'total_supplies':total_supplies,}
    return render(request, 'supplier.html', context)

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
    return render(request, 'dispatch-manager.html')


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


def profile(request):
    # profile = Profile.object.all()
    profile, created = Profile.objects.get_or_create(user=request.user)
    p_form = CustomerProfileForm(instance=profile)
    form = CustomerForm(instance=request.user)
    if request.method == "POST":
        p_form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        form = CustomerForm(request.POST, instance=request.user)
        p_form.save()
        form.save()
        messages.success(request, 'Profile updated successfully')
    # order = Order.objects.filter(customer=customer, is_active=True, completed=False).first()
    context = {+
        'p_form': p_form,
        'form': form,
        # 'order': order
    }
    return render(request, 'accounts/profile.html',  context)
