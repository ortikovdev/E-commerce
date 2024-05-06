"""
Register:
    - /register/ -> send code to user via email
    - /verify/email/ -> verify code -> activate and give token
Login:
    - /login/ -> give token
Verify Account:
    - /send/mail -> send code to user via email
    - /verify/mail -> verify code -> activate and give token
Change Password:
    - /change/password/ -> change password
Reset Password:
        - /send/mail -> send code to user via email
        - /verify/mail -> verify code -> activate and give token
    - /reset/password/ -> reset password
"""

from django.urls import path
from .views import (
    UserRegisterView,
    SendEmailView,
    VerifyEmailView,
    LoginView,
    ChangePasswordView,
    ResetPasswordView,
)

app_name = 'account'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('mail/send/', SendEmailView.as_view(), name='mail-send'),
    path('mail/verify/', VerifyEmailView.as_view(), name='mail-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('change/password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset-password'),
]


# reset password
"""
    1- Submit email form                          //PasswordResetView.as_view()
    2- Email sent success message                 //PasswordResetDoneView.as_view()
    3- Link to password Rest form in email        //PasswordResetConfirmView.as_view()
    4- Password successfully changed message      //PasswordResetCompleteView.as_view()
"""
