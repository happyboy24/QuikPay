
from wallet.services.intra_transfer import transfer_wallet_to_wallet
from notification.services import create_transfer_notification

def create_transfer(sender, receiver, amount, idempotency_key, description=None):
    transaction = transfer_wallet_to_wallet(sender, receiver, amount, idempotency_key, description)
    create_transfer_notification(receiver.user, amount)
    return transaction
