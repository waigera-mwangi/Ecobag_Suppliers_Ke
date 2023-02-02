from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        DRIVER = 'DR', _('Driver')
        FINANCE_MANAGER = 'FM', _('Finance Manager')
        INVENTORY_MANAGER = 'SM', _('Inventory Manager')
        SUPPLIER = 'RD', _('Supplier')
        CUSTOMER = 'CM', _('Customer')
        MANAGER = 'MN', _('Manager')
        BRANDER = 'BR', _('Brander')
        DISPATCH_MANAGER = 'DM', _('Dispatch Manager')

    user_type = models.CharField(
        max_length=2,
        choices=UserTypes.choices,
        default=UserTypes.CUSTOMER,
    )
    email = models.EmailField()

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

    # def create_superuser(self, email, username, password):
    #     """Creates and saves a new superuser with given details."""
    #
    #     user = self.create_user(email=email, username=username, password=password)
    #
    #     user.is_superuser = True
    #     user.is_staff = True
    #     user.save(using=self._db)


class Profile(models.Model):
    image = models.ImageField(upload_to='Users/Customers/profile_pictures/%Y/%m/',
                              default="null")
    gender = models.CharField(
        choices=GENDER_TYPES,
        default='m',
        max_length=2,
        null=True,
        blank=True
    )

    phone_number = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=False, help_text=_('Activated, users profile is published'))
    updated = models.DateTimeField(_('Updated'), auto_now=True, null=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, null=True)
    


class Customer(User):
    pass

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class CustomerProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # location = models.ForeignKey(ShipmentLocations, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customers Profile'
