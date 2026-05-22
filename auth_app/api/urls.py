from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenRefreshView
from auth_app.api.views import  RegistrationView, CookieTokenObtainPairView, CookieRefreshView, CookieDeleteView, ActivateAccountView, PasswordResetRequestView, PasswordResetConfirmView   

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path ('logout/', CookieDeleteView.as_view(), name='logout')
]