from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Wallet
from .serializer import WalletTransferSerializer, DepositSerializer, FundWalletSerializer, DashboardSerializer
from wallet.services.intra_transfer import transfer_wallet_to_wallet
from rest_framework.permissions import IsAuthenticated
from wallet.services.deposit import deposit
from notification.services import create_transfer_notification
from services.transfer_service import create_transfer
from wallet.services.fund_wallet import initiate_paystack_payment
from .services.dashboard import get_dashboard_data


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated]) #This decorator ensures that only logged in user can transfer
def wallet_transfer(request):
    sender = request.user.wallet
    serializer = WalletTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    idempotency_key = serializer.validated_data['idempotency_key']
    description=serializer.validated_data['description']

    receiver_wallet =serializer.validated_data['receiver_wallet']
    receiver = get_object_or_404(Wallet, wallet_number=receiver_wallet.pk)
    # transaction=transfer_wallet_to_wallet(sender, receiver, amount, idempotency_key, description=description)
    transaction = create_transfer(sender, receiver, amount, idempotency_key, description=description)

    create_transfer_notification(receiver.user, amount)
    return Response(
        {
         "reference": transaction.reference,
         "amount": transaction.amount,
        "status": transaction.status,
        "description": transaction.description,
        "created_at": transaction.created_at,
    }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    receiver = request.user.wallet

    serializer = DepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount = serializer.validated_data['amount']

    transaction = deposit(receiver, amount)

    create_transfer_notification(receiver.user, amount)

    return Response(
        {
            "reference": transaction.reference,
            "amount": transaction.amount,
            "status": transaction.status,
            "description": transaction.description,
            "created_at": transaction.created_at,
        }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fundd_wallet(request):
    serializer = FundWalletSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    amount = serializer.validated_data['amount']

    payment_response = initiate_paystack_payment(user, amount)

    return Response(payment_response, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    dashboard_data = get_dashboard_data(user)
    serializer = DashboardSerializer(dashboard_data)
    return Response(serializer.data, status=status.HTTP_200_OK)
