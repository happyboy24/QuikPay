
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from wallet.models import Wallet


# This class is inheriting from ModelSerializer because we are dont want to write
# explicitly the fields for this class. Since the fields have already been
# declared in the User Model. However, we will create a Meta class
# that we take only the fields we need to expose in our UserSerializer
# from the User Model. Since its not all in the fields in the User Model,
# we need here, we will collect the fields we need as a List.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     Wallet.objects.create(
    #         user=user,
    #         wallet_number=user.phone[1:]
    #     )
    #     return user

class LoginSerializer(serializers.Serializer):
    # Because we do not have a Login Model we wont do serializers.ModelSerializer
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

#         To validate if the email is a registered user
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist :
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")

        refresh = RefreshToken.for_user(user)
        data = {
            "user": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return data




