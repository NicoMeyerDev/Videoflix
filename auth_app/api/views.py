from os import link

from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """Handles user registration, creates a new user,
    and sends an activation email with a tokenized link."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()

            
            uid = urlsafe_base64_encode(force_bytes(saved_account.pk))
            token = default_token_generator.make_token(saved_account)
            link = f"http://localhost:4200/activate/{uid}/{token}/"
            send_mail(
                subject='Account aktivieren',
                message=f'Hier ist dein Aktivierungslink: {link}',
                from_email='noreply@videoflix.com', #TODO: E-Mail-Adresse anpassen
                recipient_list=[saved_account.email]
)
            data = {
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
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
            return Response({"detail": "Account activated successfully!"}, status=status.HTTP_200_OK)
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
        token = default_token_generator.make_token(user)
        link = f"http://localhost:4200/reset-password-confirm/{uid}/{token}/"
        send_mail(
            subject='Passwort zurücksetzen',
            message=f'Hier ist dein Link zum Zurücksetzen des Passworts: {link}',
            from_email='noreply@videoflix.com',
            recipient_list=[user.email]
        )
        return Response({"detail": "Password reset link sent to email"}, status=status.HTTP_200_OK)

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
            return Response({"detail": "Password reset successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password reset link"}, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handles the login process, generates access and refresh tokens,
    and stores both as HttpOnly cookies in the response.
    """

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except:
            return Response(
                {"detail": "Ungültige Anmeldedaten."},
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        

       

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
        user = User.objects.get(username=request.data.get('username'))
    


        response.data = {"detail": "Login successfully!", "user": {"id": user.id, "username": user.username, "email": user.email   }}
        return response
    
    
class CookieRefreshView(TokenRefreshView):
    """
    Refreshes the access token using a refresh token stored in a cookie
    and sets the new access token as an HttpOnly cookie in the response.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        #refresh token nicht im Cookie gefunden
        if refresh_token is None:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED)   
        
        serializer =self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:    
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        access_token = serializer.validated_data.get('access')
        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
    
class CookieDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    """
    Handles the logout process by deleting the access and refresh token cookies.
    """

    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
        