import uuid

from django.db import models

from Quickpay import settings
from wallet.util import generate_account_number, generate_reference_number


# Create your models here.

class Wallet(models.Model):
    CURRENCY_CHOICES = (
    ('NGN', 'Naira'),
    ('USD', 'Dollar'),
    ('EUR', 'Euro'),
    )
    WALLET_STAUS = (
        ( 'ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        ('SUSPENDED', 'SUSPENDED'),
        ('CLOSED', 'CLOSED'),
        ('FROZEN', 'FROZEN')
    )
    wallet_number = models.CharField(max_length=10, unique=True)
    account_number = models.CharField(max_length=10, unique=True, default= generate_account_number())
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #here in my settings.py i have created my own models from class User
    #and here am importing it telling the wallet to use it (settings.AUTH_USER_MODEL)
    #model.PROTECT am saying that you cant delete records
    #but with CASCADE i can be able to delete records, IF I DELETE THE PARENT THE CHILD SHOULD BE DELETED

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )
    TRANSACTION_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
    )

    reference = models.CharField(max_length=35, default= generate_reference_number())
    transaction_type = models.CharField(max_length=6, choices = TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='sender')
    receiver = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='receiver')
    status = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, blank=False, null=False)


class Ledger(models.Model):
    ENRTY_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=6, choices = ENRTY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
