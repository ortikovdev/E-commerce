from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from apps.account.models import User


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
