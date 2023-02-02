from django.contrib import admin

from .models import (
    LoanApplication,
    LoanRepayment,
    Savings)

admin.site.register(LoanApplication)
admin.site.register(LoanRepayment)
admin.site.register(Savings)

