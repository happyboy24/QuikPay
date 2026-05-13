from django.contrib import admin




from .models import Wallet, Transaction, Ledger

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['wallet_number', 'account_number',  'balance', 'currency', 'status']
    list_editable = ['status']
    list_per_page = 10


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'amount', 'status', 'created_at']
    list_per_page = 10


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'amount', 'balance_after', 'entry_type', 'created_at']






