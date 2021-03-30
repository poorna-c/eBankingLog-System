from django.urls import path
from .views import create_user, dashboard, transfer_funds, payment, transactions, account_details, complete_transaction, home
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',create_user, name = 'register_page'),
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'),name = 'login_page'),
    path('profile/',dashboard,name='dashboard_page'),
    path('transfer_funds/',transfer_funds,name='transfer_funds_page'),
    path('payment/',payment,name='payment_page'),
    path('transactions/',transactions,name='transactions_page'),
    path('account_details/',account_details,name='account_details_page'),
    path('complete_transaction/',complete_transaction,name='complete_transaction_page'),
    path('logout/',auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name = 'logout'),
    path('',home, name='home_page')
]