from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.
class BankAccounts(models.Model):
    user_link = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30)
    account_no = models.DecimalField(max_digits=8, decimal_places=0)
    account_balance = models.DecimalField(max_digits=8, decimal_places=2)
    mobile_number = models.DecimalField(max_digits=10, decimal_places=0)

class PastTransactions(models.Model):
    account_no_link = models.ManyToManyField(BankAccounts)
    date_time = models.DateTimeField(default=datetime.datetime.now())
    transaction_description = models.CharField(max_length=30)
    amount = models.DecimalField(default = 0, null=True ,blank=True,max_digits=8,decimal_places=2)
    transaction_type = models.CharField(max_length = 6, null=True,blank=True, choices=(('CREDIT','CREDIT'),('DEBIT','DEBIT')))



