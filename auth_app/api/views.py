from urllib import request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives

from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.exceptions import (InvalidToken,TokenError)
from rest_framework.exceptions import AuthenticationFailed
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """Handles user registration, creates a new user,
    and sends an activation email with a tokenized link."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            saved_account = serializer.save()
            saved_account.is_active = False
            saved_account.save()

            uid = urlsafe_base64_encode(force_bytes(saved_account.pk))
            token = default_token_generator.make_token(saved_account).replace('=', '')
            
            link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uid}&token={token}"

            text_content = f"Activate your account: {link}"
            html_content = render_to_string('activation_email.html', {'user_email': saved_account.email,'link': link},
            )
            msg = EmailMultiAlternatives(
                subject='Confirm your Account',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[saved_account.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response({"user": {"id": saved_account.pk, "email": saved_account.email}, "token": token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ActivateAccountView(APIView):
    """Handles account activation by validating the token
    from the activation link and activating the user's account."""
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account successfully activated!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)        

class PasswordResetRequestView(APIView):
    """Handles password reset requests by validating the email,
    generating a tokenized link, and sending it to the user's email."""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user).replace('=', '')
        link = f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uid}&token={token}"

        text_content = f"Reset your password: {link}"
        html_content = render_to_string('password_reset_email.html', {'link': link})
        msg = EmailMultiAlternatives(
            subject='Password Reset Request',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    """Handles password reset confirmation by validating the token from the reset link
    and allowing the user to set a new password."""
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({"detail": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Your Password has been successfully reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password reset link"}, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handles the login process, generates access and refresh tokens,
    and stores both as HttpOnly cookies in the response.
    """

    def post(self, request, *args, **kwargs):
        """
        Overrides the default TokenObtainPairView post method.
        Accepts email instead of username for authentication.
        On success, stores access and refresh tokens as HttpOnly cookies
        and sets the CSRF token as a non-HttpOnly cookie for frontend use.
        Returns user data without exposing the tokens in the response body.
        """

        request.data["username"] = request.data.get("email")

        try:
            response = super().post(request, *args, **kwargs)
        except (AuthenticationFailed, InvalidToken, TokenError):
            return Response(
                {"detail": "Ungültige Anmeldedaten."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = response.data.get("refresh")
        access = response.data.get("access")
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',    
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        User = get_user_model()
        user = User.objects.get(username=request.data.get('email'))
    
        response.data = {"detail": "Login successfully!", "user": {"id": user.id, "username": user.username}}
        csrf_token = get_token(request)

        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=True,
            samesite="Lax"
        )
        return response
    
    
class CookieRefreshView(TokenRefreshView):
    """
    Refreshes the access token using a refresh token stored in a cookie
    and sets the new access token as an HttpOnly cookie in the response.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token is None:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)   
        
        serializer =self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:    
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data.get('access')
        response = Response({"detail": "Token refreshed", "access": access_token})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
    
class CookieDeleteView(APIView):
    permission_classes = [AllowAny]
    """
    Handles the logout process by deleting the access and refresh token cookies.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token fehlt."}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
        