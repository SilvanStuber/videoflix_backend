from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


class RegistrationView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        request.data['username'] = generate_username(request)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            send_confirmation_email(saved_account)
            return Response({"message": "Bitte überprüfe deine E-Mails, um deinen Account zu aktivieren."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Bitte überprüfe deine Eingaben und versuche es erneut."}, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccountView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Dein Account wurde erfolgreich aktiviert."}, status=status.HTTP_200_OK)
            return Response({"error": "Ungültiger oder abgelaufener Token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Aktivierungsfehler."}, status=status.HTTP_400_BAD_REQUEST)


def generate_username(request):
    username = request.data.get('username', '') 
    if ' ' in username:
            username = username.replace(' ', '_')
    return username.lower()

def send_confirmation_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    full_link = f"http://localhost:8000{activation_link}"
    subject = "Bestätige deinen Videoflix-Account"
    message = generate_email(user.username, full_link)
    send_mail(subject, message, 'mail@silvanstuber.ch', [user.email])

def generate_email(username, full_link):
    html_message = f"""
    <p>Hallo {username},</p>
    <p>Bitte aktiviere deinen Videoflix-Account, indem du auf den folgenden Link klickst:</p>
    <p><a href="{full_link}">Account aktivieren</a></p>
    <p>Vielen Dank, dass du dich für Videoflix entschieden hast!</p>
    """
    return html_message