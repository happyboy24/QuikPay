from django.shortcuts import get_object_or_404

from wallet.models import Wallet
from .models import Notification
from django.core.mail import send_mail


def create_notification(user):
    notification = Notification.objects.create(
        # user=user,
        wallet=user.wallet.wallet_number,
        message=f""" 
        Hi {user.first_name} Welcome to QuickPay!
        Your wallet number is: {user.wallet.wallet_number}
        Your alternate wallet number is: {user.wallet.account_number}

        Thank you for using QuickPay!
        """,

            event_type='USER_WALLET_CREATED',
    )

    send_mail(
        subject="Welcome to QuickPay!",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()


def create_transfer_notification(user, amount):
    wallet = get_object_or_404(Wallet, user=user)
    notification = Notification.objects.create(
        wallet=user.wallet.wallet_number,
        message=f"""***CREDIT ALERT***
        {amount} has been credited to your wallet.
        your new balance is {wallet.balance}
    """,
        event_type='USER_TRANSFER_NOTIFICATION',
    )

    send_mail(
        subject="Wallet Transfer Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()



def deposit_notification(user, amount):
    wallet = get_object_or_404(Wallet, user=user)
    notification = Notification.objects.create(
        wallet=user.wallet.wallet_number,
        message=f"""***DEPOSIT SUCCESSFUL***
            {amount} has been credited to your wallet.
            your new balance is {wallet.balance}
        """,
        event_type='WALLET_DEPOSIT_NOTIFICATION',
    )

    send_mail(
        subject="Wallet Deposit Notification",
        message=notification.message,
        from_email='',
        recipient_list=[user.email],
        fail_silently=True
    )
    notification.is_read = True
    notification.save()




