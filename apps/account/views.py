from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.tasks import ecommerce_send_email
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.account.models import User, UserToken
from apps.account.serializers import (
    UserRegisterSerializer,
    SendEmailSerializer,
    VerifyEmailSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
)
from .permissions import IsOwnerOrReadOnly



class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = UserToken.objects.create(user=user)
        print(("Activation Token Code", token.token, [user.email]))
        ecommerce_send_email.apply_async(("Activation Token Code", str(token.token), [user.email]),)
        data = {
            'success': True,
            'detail': 'Activation Token Code has been sent to your email.'
        }
        return Response(data, status=status.HTTP_201_CREATED)


class SendEmailView(generics.CreateAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']

        user = get_object_or_404(User, email=email)
        token = UserToken.objects.create(user=user)
        ecommerce_send_email.apply_async(("Activation Token Code", str(token.token), [user.email]),)
        data = {
            'success': True,
            'detail': 'Activation Token Code has been sent to your email.'
        }
        return Response(data, status=status.HTTP_200_OK)


class VerifyEmailView(generics.CreateAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        refresh = RefreshToken.for_user(user)
        obtain_tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(obtain_tokens, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    pass


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'detail': 'Your password has been changed.'
        }
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'detail': 'Your password has been reset.'
        }
        return Response(data, status=status.HTTP_200_OK)


class UserProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsOwnerOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        data = {
            'success': True,
            'detail': 'Your account has been deactivated successfully.'
        }
        return Response(data, status=status.HTTP_200_OK)
