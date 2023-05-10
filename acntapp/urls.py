from django.urls import path,include
from .views import UserRegistrationView,LoginView,UserProfileView,UserChangePassword,PasswordResetEmail,PasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePassword.as_view(),name='change_password'),
    path('passwordresetemail/',PasswordResetEmail.as_view(),name='send-reset-password-email'),
    path('reset-password/uid/<token>/',PasswordResetView.as_view(),name='reset_password'),


]


