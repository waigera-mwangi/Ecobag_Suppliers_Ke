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
                messages.warning(request, 'Invalid Login credentials ')
                # msg = messages.error(request, 'Invalid form submission')
        else:
            messages.warning(request, 'Invalid form submission')
            msg = 'Invalid form submission'

    return render(request, 'accounts/user-login.html', {'form': loginform, 'msg': msg})


@required_access(login_url=reverse_lazy('accounts:login'), user_type="CM")
def customer(request):

    return redirect('store:view-product')



@required_access(login_url=reverse_lazy('accounts:login'), user_type="SM")
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
    orders = Order.objects.all()
    # approved = orders.filter(orderstatus='Approved').count()
    context = {
               #context
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
    
   
    context = {
              #content of the context

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



class FAQQuestionTypeListView(ListView):
    template_name = 'faq/customer_faq.html'
    queryset = FAQ.objects.filter(question_types='CM')
    context_object_name = 'faqs'

class D_FAQ(ListView):
    template_name = 'faq/driver_faq.html'
    queryset = FAQ.objects.filter(question_types='DR')
    context_object_name = 'faqs'

class S_FAQ(ListView):
    template_name = 'faq/supplier_faq.html'
    queryset = FAQ.objects.filter(question_types='RD')
    context_object_name = 'faqs'

class B_FAQ(ListView):
    template_name = 'faq/brander_faq.html'
    queryset = FAQ.objects.filter(question_types='BR')
    context_object_name = 'faqs'

class I_FAQ(ListView):
    template_name = 'faq/inventory_faq.html'
    queryset = FAQ.objects.filter(question_types='SM')
    context_object_name = 'faqs'

class DP_FAQ(ListView):
    template_name = 'faq/dispatch_faq.html'
    queryset = FAQ.objects.filter(question_types='DM')
    context_object_name = 'faqs'

class F_FAQ(ListView):
    template_name = 'faq/finance_faq.html'
    queryset = FAQ.objects.filter(question_types='FM')
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
    profile_image_url = customer_profile.image.url if customer_profile.image else None
    
    if request.method == "POST":
        p_form = CustomerProfileForm(request.POST, request.FILES, instance=customer_profile)
        form = CustomerForm(request.POST, instance=request.user)
        
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:customer')
    context = {
        'p_form': p_form,
        'form': form,
        'customer_profile': customer_profile,
        'profile_image_url': profile_image_url,
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
            return redirect('accounts:finance-manager')
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
            return redirect('accounts:brander')
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
            return redirect('accounts:dispatch-manager')
    context = {
        'p_form': p_form,
        'form': form,
        'dispatch_profile': dispatch_profile,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'accounts/profiles/dispatch-profile.html',  context)

def driver_profile(request):

    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
    # handle the case where no profile exists for the user
        driver_profile = DriverProfile.objects.create(user=request.user)

    p_form = DriverProfileForm(instance=driver_profile)
    form = DriverForm(instance=request.user)

    # Retrieve profile image URL
    profile_image_url = driver_profile.image.url if driver_profile.image else None
    

    if request.method == "POST":
        p_form = DriverProfileForm(request.POST, request.FILES, instance=driver_profile)
        form = DriverForm(request.POST, instance=request.user)
        if p_form.is_valid() and form.is_valid():
            p_form.save()
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('accounts:driver')

    context = {
        'p_form': p_form,
        'form': form,
        'driver_profile': driver_profile,
        'profile_image_url': profile_image_url,
        
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
            return redirect('accounts:inventory')
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
            return redirect('accounts:supplier')

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

# password reset
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    
    def get_success_url(self):
            return reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


# customer feedback view
def customer_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/customer_feedback.html', {'conversations': conversations,})

# finance feedback views
def finance_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/finance_feedback.html', {'conversations': conversations,})

# inventory feedback views
def inventory_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/inventory_feedback.html', {'conversations': conversations,})

# brander feedback views
def brander_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/brander_feedback.html', {'conversations': conversations,})

# dispatch feedback views
def dispatch_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/dispatch_feedback.html', {'conversations': conversations,})

# supplier feedback views
def supplier_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/supplier_feedback.html', {'conversations': conversations,})

#driver customer feedback views
def driver_feedback_view(request):
    # Retrieve conversations for the current user
    conversations = Feedback.objects.filter(sender=request.user) | Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback/view_feedback/driver_feedback.html', {'conversations': conversations,})

# customer feedback submission
def customer_send_feedback_view(request):
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:customer_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = CustomerFeedbackForm()
    
    return render(request, 'feedback/send_feedback/customer_send_feedback.html', {'form': form})

# finance feedback submission
def finance_send_feedback_view(request):
    if request.method == 'POST':
        form = FinanceFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:finance_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = FinanceFeedbackForm()
    
    return render(request, 'feedback/send_feedback/finance_send_feedback.html', {'form': form})

# inventory feedback submission
def inventory_send_feedback_view(request):
    if request.method == 'POST':
        form = InventoryFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:inventory_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = InventoryFeedbackForm()
    
    return render(request, 'feedback/send_feedback/inventory_send_feedback.html', {'form': form})

# brander feedback submission
def brander_send_feedback_view(request):
    if request.method == 'POST':
        form = BranderFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:brander_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = BranderFeedbackForm()
    
    
    return render(request, 'feedback/send_feedback/brander_send_feedback.html', {'form': form})

# supplier feedback submission
def supplier_send_feedback_view(request):
    if request.method == 'POST':
        form = SupplierFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:supplier_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = SupplierFeedbackForm()
    
    return render(request, 'feedback/send_feedback/supplier_send_feedback.html', {'form': form})

# dispatch feedback submission
def dispatch_send_feedback_view(request):
    if request.method == 'POST':
        form = DispatchFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:dispatch_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = DispatchFeedbackForm()
    
    return render(request, 'feedback/send_feedback/dispatch_send_feedback.html', {'form': form})

# driver feedback submission
def driver_send_feedback_view(request):
    if request.method == 'POST':
        form = DriverFeedbackForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            message = form.cleaned_data['message']

            Feedback.objects.create(sender=request.user, receiver=receiver, message=message)
            
            # Add success message
            messages.success(request, 'Feedback sent successfully!')
            
            return redirect('accounts:driver_feedback')
        else:
            # Add warning message for form errors or empty fields
            messages.warning(request, 'Please correct the form errors and fill in all fields.')
    else:
        form = DriverFeedbackForm()
    
    return render(request, 'feedback/send_feedback/driver_send_feedback.html', {'form': form})

def about_us(request):
    return render(request, 'includes/about-us.html')