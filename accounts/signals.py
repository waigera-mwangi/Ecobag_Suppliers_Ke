from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# @receiver(pre_save, sender=User)
# def update_is_active(sender, instance, **kwargs):
#     # Check if the instance being saved is a new user (not an existing one being updated)
#     if instance._state.adding:
#         # If it's a new user, check if it's a superuser
#         if instance.is_superuser:
#             # If it's a superuser, set is_active to True
#             instance.is_active = True
#         else:
#             # If it's not a superuser, set is_active to False
#             instance.is_active = False


@receiver(pre_save, sender=User)
def update_is_active(sender, instance, **kwargs):
    if instance._state.adding and instance.is_superuser:
        instance.is_active = True