from django.db import models

# class OrderPayment(models.Model):
#     transaction_id = models.CharField(max_length=250)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     mpesa = models.CharField(max_length=10, help_text="Mpesa Code e.g MXFTR432R5")
#     phone = models.IntegerField(blank=True, null=True)
#     # manager = models.ForeignKey(Finance Man, on_delete=models.CASCADE, null=True)
#     amount = models.FloatField(default=0.0)
#     confirmed = models.BooleanField(default=False, help_text="Means manager has confirmed payment")
#     updated = models.DateTimeField(('Updated'), auto_now=True, null=True)
#     created = models.DateTimeField(('Created'), auto_now_add=True, null=True)