from django.contrib import admin
from .models import BankAccounts, PastTransactions

# Register your models here.
admin.site.register(BankAccounts)
admin.site.register(PastTransactions)
