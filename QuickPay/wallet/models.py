import uuid

from django.db import models


from django.conf import settings
user = settings.AUTH_USER_MODEL
#This is done to prevent tight-coupling between
#the user Module and this wallet Module

from wallet.util import generate_wallet_number, generate_reference


# Create your models here.

class Wallet(models.Model):
    CURRENCY_CHOICES = (
        ('NGN', 'Naira'),
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
    )

    WALLET_STATUS=(
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('CLOSED', 'Closed'),
        ('FROZEN', 'Frozen'),
    )

    user = models.OneToOneField(user, on_delete=models.PROTECT)
    #with on_delete as PROTECT both the parent class and the child class
    #cannot be deleted.
    #with on_delete as CASCADE, if the parent class is deleted, the child
    #class is also deleted, however, if the parent class is still available
    #and you want to delete the child class, it wouldn't be allowed.
    wallet_number = models.CharField(max_length=10, unique=True, primary_key=True)
    account_number = models.CharField(max_length=10, unique=True, default=generate_wallet_number())
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="NGN")
    status = models.BooleanField(default=True) #Every wallet is active by default
    created_at = models.DateTimeField(auto_now_add=True) #Stores only at creation

    def __str__(self):
        return f"{self.wallet_number}"

#We are having the Wallet, Transaction, and LedgerEntry in same
#module because, they belong to the same domain.
#If they are in different modules/app scaling will be difficult
#and there will be alot of tight coupling because we want to record
#every transaction that occurred in a wallet, and register every
#money movement that happens in the wallet in the LedgerEntry


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )
    TRANSACTION_STATUS = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    reference = models.CharField(max_length=100, default=generate_reference())
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="sender")

    # If you look at the first arg above for sender,
    # the Wallet wasn't imported because the Wallet class
    # is still in this same
    # This is the importance of grouping entities of the same domain
    # in one module.

    receiver = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="receiver")
    status = models.CharField(max_length=7, choices=TRANSACTION_STATUS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.UUIDField(unique=True, editable=False, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

class Ledger(models.Model):
    TRANSACTION_TYPE  = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction}  {self.entry_type} {self.amount}"









