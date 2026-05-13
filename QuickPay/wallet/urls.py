from django.urls import path


from .views import wallet_transfer, fund_wallet, fundd_wallet, dashboard
from wallet.services.fund_wallet import paystack_callback

urlpatterns = [
    path('transfer/', wallet_transfer, name='transfer'),
    path('deposit/', fund_wallet, name='deposit'), #classworkDoneByMe

    path('callback/', paystack_callback, name='paystack_callback'),

    path('fund/', fundd_wallet, name='fund_wallet'),

    path("dashboard/", dashboard, name="dashboard")#DoneWithMrSk
]

