from notification.services import create_notification
from wallet.services.create_wallet import create_wallet
from user.services import create_user
from django.db import transaction
from notification.services import create_notification

# Since we are creating a User and a Wallet at the same time,
# we use @transaction.atomic.
# This ensures that if the Wallet fails to create,
# the User creation is rolled back so you don't end up with "orphaned" users without wallets.

@transaction.atomic
def create_user_and_wallet(validated_data):
    user = create_user(validated_data)
    wallet = create_wallet(user)
    create_notification(user)
    return user, wallet