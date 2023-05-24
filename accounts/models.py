from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class CustomPhoneNumberField(PhoneNumberField):
    default_error_messages = {
        'invalid': 'Please enter a valid phone number in the format +254723000000.',
    }

class TimeStamp(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class User(AbstractUser, PermissionsMixin):
    class UserTypes(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance Manager')
        INVENTORY_MANAGER = 'SM', _('Inventory Manager')
        SUPPLIER = 'RD', _('Supplier')
        CUSTOMER = 'CM', _('Customer')
        MANAGER = 'MN', _('Manager')
        BRANDER = 'BR', _('Brander')
        DISPATCH_MANAGER = 'DM', _('Dispatch Manager')
        ADMIN = 'AD', _('Admin')

    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
        default=UserTypes.CUSTOMER,
    )
    first_name = models.CharField( max_length=250, null=True)
    last_name = models.CharField( max_length=250, null=True)
    phone_number = CustomPhoneNumberField(null=True, unique=True)
    id_number = models.IntegerField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def get_user_type_display(self):
        return dict(User.UserTypes.choices)[self.user_type]


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



# customer profile model

GENDER_TYPES = (
    ('m', 'Male'),
    ('f', 'Female')
)




class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, username, password=None):
        """Creates a user profile object."""

        if not email:
            raise ValueError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.user_id = -1
        user.set_password(password)
        user.save(using=self._db)

        return user


class TimeStamp(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')

    image = models.ImageField(upload_to='Users/profile_pictures/%Y/%m/',
                              default="null")
    phone_number = PhoneNumberField(null=False)
    is_active = models.BooleanField(_('Active'), default=True, help_text=_('Activated, users profile is published'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.FEMALE,
    )
    


class CustomerProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customers Profile'

class FinanceProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='finance_profile')
    class Meta:
        verbose_name = 'Finance Profile'
        verbose_name_plural = 'Finance Profiles'

class InventoryProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inventory_profile')
    class Meta:
        verbose_name = 'Inventory Profile'
        verbose_name_plural = 'Inventorie Profiles'

class SupplyProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile')
    class Meta:
        verbose_name = 'Supplier Profile'
        verbose_name_plural = 'Supplier Profiles'

class BranderProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brander_profile')
    class Meta:
        verbose_name = 'Brander Profile'
        verbose_name_plural = 'Brander Profiles'

class DispatchProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dispatch_profile')
    class Meta:
        verbose_name = 'Dispatch Profile'
        verbose_name_plural = 'Dispatch Profiles'

class DriverProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    class Meta:
        verbose_name = 'Driver Profile'
        verbose_name_plural = 'Driver Profiles'


class Customer(User):
    pass

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class Finance(User):
    pass

    class Meta:
        verbose_name = 'Finance'
        verbose_name_plural = 'Finance'

class Supply(User):
    pass

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

class Dispatch(User):
    pass

    class Meta:
        verbose_name = 'Dispatch_Manager'
        verbose_name_plural = 'Dispatch_Managers'

class Inventory(User):
    pass

    class Meta:
        verbose_name = 'Inventory'

class Driver(User):
    pass

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

class Brander(User):
    pass

    class Meta:
        verbose_name = 'Brander'
        verbose_name_plural = 'Branders'

        #Faqs 

#Faqs 
class FAQ(TimeStamp):
    class QustionType(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance Manager')
        INVENTORY_MANAGER = 'SM', _('Inventory Manager')
        SUPPLIER = 'RD', _('Supplier')
        CUSTOMER = 'CM', _('Customer')
        MANAGER = 'MN', _('Manager')
        BRANDER = 'BR', _('Brander')
        DISPATCH_MANAGER = 'DM', _('Dispatch Manager')
        
    question_types = models.CharField(
        _('question Type'),
        max_length=3,
        choices=QustionType.choices,
        default=QustionType.CUSTOMER
    )
    subject = models.CharField( max_length=250, null=True)
    content = models.TextField(null=True)
