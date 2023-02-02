from django.db import models


class LoanApplication(models.Model):
    STATUS_CHOICE = (
        ('pg', 'Pending'),
        ('dc', 'Decline'),
        ('ap', 'Approved'),
        ('pr', 'Processing'),
    )
    amount = models.IntegerField(20)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True)
    limit = models.IntegerField(null=True)
    purpose = models.TextField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Pending')


class Savings(models.Model):
    amount = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)


class LoanRepayment(models.Model):
    amount = models.IntegerField(20)
    created_date = models.DateField(auto_now_add=True)
    balance = models.IntegerField()
