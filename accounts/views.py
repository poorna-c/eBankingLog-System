from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import BankAccounts, PastTransactions

from twilio.rest import Client
import random

# Create your views here.
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    form = UserCreationForm()
    return render(request,'accounts/register.html',{'form':form})

def dashboard(request):
    logged_in_user = request.user
    ba = BankAccounts.objects.get(user_link=logged_in_user)
    return render(request,'accounts/profile.html',{'logged_in_user':logged_in_user,'balance':ba.account_balance})

def transactions(request):
    logged_in_user = request.user
    ba = BankAccounts.objects.get(user_link=logged_in_user)
    transactions = PastTransactions.objects.filter(account_no_link=ba)
    return render(request,'accounts/transactions.html',{'transactions':transactions})

def home(request):
    return render(request,'accounts/home.html')

def account_details(request):
    u = request.user
    mail = u.email
    ba = BankAccounts.objects.filter(user_link=u).first()
    name = ba.name
    acc_no = ba.account_no
    acc_bal = ba.account_balance
    return render(request,'accounts/account_details.html',{'uname':u,'mail':mail,'name':name,'acc_no':acc_no,'acc_bal':acc_bal})

def transfer_funds(request):
    balance = BankAccounts.objects.filter(user_link=request.user).first().account_balance
    return render(request,'accounts/transfer_funds.html',{'balance':balance})

def payment(request):
    if request.method == 'POST':
        to_acc = int(request.POST.get('to_acc'))
        ifsc = request.POST.get("ifsc")
        amt = request.POST.get('amt')

        to_bank_acc = BankAccounts.objects.get(account_no=to_acc)
        if to_bank_acc:
            sent_otp = send_otp(to_bank_acc.mobile_number)
            return render(request,'accounts/payment.html',{'amt':amt,'to_acc':to_acc,'ifsc':ifsc,'sent_otp':send_otp})
        else:
            return render(request,'accounts/transfer_funds.html')

    return render(request,'accounts/payment.html')


def complete_transaction(request):
    if request.method == 'POST':
        to_acc = BankAccounts.objects.get(account_no= int(request.POST.get('to_acc')))
        ifsc = request.POST.get("ifsc")
        amt = int(request.POST.get('amt'))

        from_acc = BankAccounts.objects.get(user_link=request.user)
        from_acc.account_balance -= amt
        from_acc.save()
        pt_from_acc = PastTransactions(transaction_description="Being Transfer to "+str(to_acc.name),amount=amt,transaction_type="DEBIT")
        pt_from_acc.save()
        pt_from_acc.account_no_link.add(from_acc)
        pt_from_acc.save()

        to_acc.account_balance += amt
        to_acc.save()
        pt_to_acc = PastTransactions(transaction_description="Being Transfer from "+str(from_acc.name),amount=amt,transaction_type="CREDIT")
        pt_to_acc.save()
        pt_to_acc.account_no_link.add(to_acc)
        pt_to_acc.save()

        logged_in_user = request.user
        ba = BankAccounts.objects.get(user_link=logged_in_user)
        
        return redirect('dashboard_page')

        


def send_otp(mobile):
    otp = ''.join([str(random.randint(0,9)) for i in range(6)])
    account_sid = '[YOUR ACCOUNT SID]' 
    auth_token = '[YOUR AUTH TOKEN]' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(messaging_service_sid='[YOUR MSG SERVICE SID]', to='+91'+str(mobile),body='Your OTP is '+ str(otp))
    print(message.sid,"OTP SENT TO",mobile)
    return otp
