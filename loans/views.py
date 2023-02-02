from django.shortcuts import render, redirect

from loans.forms import LoanApplicationForm


# Create your views here.
def Apply_loan(request):
    forms = LoanApplicationForm()
    if request.method == 'POST':
        forms = LoanApplicationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'finance/loan-application.html', context)
