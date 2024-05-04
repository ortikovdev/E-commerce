import email

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.account.models import User, UserToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password], help_text='password_validators')
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email already registered.'})
        if password1 != password2:
            raise ValidationError("Passwords did not match")
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(password1)
        user.save()
        return user


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email does not exist.'})
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.IntegerField()

    class Meta:
        fields = ['email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')

        if UserToken.objects.filter(user__email=email).exists():
            user_token = UserToken.objects.filter(user__email=email).last()
            if user_token.is_used:
                raise ValidationError({'email': 'Verification code is already used.'})
            if token != user_token.token:
                raise ValidationError({'email': 'Token does not match'})
            user_token.is_used = True
            user = User.objects.get(email=email)
            user_token.is_active = True
            user_token.save()
            user.save()
            return attrs

        raise ValidationError({'email': 'Credentials are not valid'})


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['created_date'] = user.created_date.strftime('%d.%m.%Y %H:%M:%S')
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['old_password', 'password', 'new_password']

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        new_password = attrs.get('password2')

        if self.context['faa'].user.check_password(old_password):
            if password == new_password:
                return attrs
            raise ValidationError('Passwords did not match')
        raise ValidationError({'old_password': 'old password did not match'})

    def create(self, validated_data):
        password = validated_data.get('password')
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

