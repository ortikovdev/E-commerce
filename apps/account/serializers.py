import email

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
    class Meta:
        fields = ['email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')

        if UserToken.objects.filter(email=email, token=token).exists():
            user_token = UserToken.objects.filter(email__email=email).last()
            if user_token.is_used:
                raise ValidationError({'email': 'Verification code is already used.'})
            if token != user_token.token:
                raise ValidationError({'email': 'Token does not match'})
            user_token.is_used = True
            user = User.objects.get(email=email)
            user_token.is_active = True
            user_token.save()
            user.save()

        raise ValidationError({'email': 'Credentials are not valid'})