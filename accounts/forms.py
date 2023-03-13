from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model, logout
from django.forms import forms, ModelForm
from django import forms
from accounts.models import Profile
from accounts.models import CustomerProfile, Customer

User = get_user_model()


class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "CM"
        if commit:
            user.save()
        return user


class CustomerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and self.user_cache.is_staff or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "FM" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "RD":
            logout(self.request)
            raise forms.ValidationError('Invalid Username or Password ', code='invalid login')


class SupplierSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "CM"
        if commit:
            user.save()
        return user


class SupplierAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and self.user_cache.is_staff or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "FM" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM" or self.user_cache.user_type == "MN" or \
                self.user_cache.user_type == "BR" or self.user_cache.user_type == "DM":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password', code='invalid login')


class FinanceManagerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None  or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "RD" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')

class ManagerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None  or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "RD" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM" or self.user_cache.user_type == "BR" or \
                self.user_cache.user_type == "DM":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')

class BranderAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None  or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "RD" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM" or self.user_cache.user_type == "BR" \
                or self.user_cache.user_type == "MN":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')

class DispatchManagerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None  or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "RD" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM" or self.user_cache.user_type == "MN" or \
                self.user_cache.user_type == "BR":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')


class SalesManagerAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and self.user_cache.is_staff or self.user_cache.user_type == "DR" or \
                self.user_cache.user_type == "FM" or self.user_cache.user_type == "RD" or \
                self.user_cache.user_type == "CM":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')


class DriverAuthenticationForm(AuthenticationForm):

    def clean(self):
        super().clean()
        if self.user_cache is not None and self.user_cache.is_staff or self.user_cache.user_type == "RD" or \
                self.user_cache.user_type == "FM" or self.user_cache.user_type == "SM" or \
                self.user_cache.user_type == "CM":
            logout(self.request)
            raise forms.ValidationError('Invalid username or password ', code='invalid login')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['image', 'gender', 'phone_number']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['last_name', 'first_name', 'email']

# overiding password
class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'user_type', 'password1', 'password2']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.upper()

class UserAdminChangeForm(ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admins
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_active']

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.upper()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
