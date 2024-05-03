from rest_framework import generics, status
from rest_framework.response import Response

from .tasks import send_password_reset_email
from apps.account.models import User, UserToken
from apps.account.serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = UserToken.objects.create(user=user)
        print(("Activation Token Code", token.token, [user.email]))
        send_password_reset_email.apply_async(("Activation Token Code", token.token, [user.email]),)
        data = {
            'success': True,
            'detail': 'Activation Token Code has been sent to your email.'
        }
        return Response(data, status=status.HTTP_201_CREATED)