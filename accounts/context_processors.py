from .models import *
def profiles(request):
    context = {}
    if request.user.is_authenticated:
       
        try:
            context['customer_profile'] = request.user.customer_profile
        except CustomerProfile.DoesNotExist:
            pass
    #     try:
    #         context['finance_profile'] = request.user.finance_profile
    #     except FinanceProfile.DoesNotExist:
    #         pass
    #     try:
    #         context['inventory_profile'] = request.user.inventory_profile
    #     except InventoryProfile.DoesNotExist:
    #         pass
    #     try:
    #         context['service_provider_profile'] = request.user.service_provider_profile
    #     except ServiceProviderProfile.DoesNotExist:
    #         pass
    #     try:
    #         context['supplier_profile'] = request.user.supplier_profile
    #     except SupplyProfile.DoesNotExist:
    #         pass
    #     try:
    #         context['driver_profile'] = request.user.driver_profile
    #     except DriverProfile.DoesNotExist:
    #         pass
    # return context




# def unread_message_count(request):
#     if request.user.is_authenticated:
#         count = Message.objects.filter(recipient=request.user, read=False).count()
#     else:
#         count = 0
#     return {'unread_message_count': count}
