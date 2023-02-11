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
from accounts.forms import CustomerSignUpForm, CustomerAuthenticationForm, SupplierSignUpForm, SupplierAuthenticationForm, \
    StaffLoginForm, CustomerProfileForm, CustomerForm
from accounts.models import User, CustomerProfile, Profile
from django.urls import reverse_lazy

from store.models import Order


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/customer-registration.html"
    form_class = CustomerSignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('index')


class CustomerLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/customer-login.html'
    authentication_form = CustomerAuthenticationForm
    success_url = reverse_lazy('index')
    success_message = "You've logged in successfully"


class LogoutView(View):

    def get(self, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, "You've logged out successfully.")
        return redirect('index')


class SupplierCreateView(SuccessMessageMixin, CreateView):
    template_name = "accounts/Supplier-registration.html"
    form_class = SupplierSignUpForm
    model = User
    success_message = "You've registered successfully"
    success_url = reverse_lazy('Supplier')


class SupplierLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/Supplier-login.html'
    authentication_form = SupplierAuthenticationForm
    success_url = reverse_lazy('Supplier')
    success_message = "You've logged in successfully"


def staff_login_view(request):
    loginform = StaffLoginForm(request.POST or None)
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

            elif user is not None and user.user_type == "DR":
                login(request, user)
                return redirect('accounts:driver')

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
    return render(request, 'accounts/staff-login.html', {'form': loginform, 'msg': msg})


@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="SM")
def inventory_manager(request):
    return render(request, 'inventory-manager.html')


@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="FM")
def finance_manager(request):
    return render(request, 'finance-manager.html')


@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="DR")
def driver(request):
    return render(request, 'driver.html')

@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="MN")
def manager(request):
    return render(request, 'manager.html')

@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="BR")
def brander(request):
    return render(request, 'brander.html')

@required_access(login_url=reverse_lazy('accounts:staff-login'), user_type="DM")
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
