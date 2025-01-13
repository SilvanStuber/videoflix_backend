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
from django.http import HttpResponseRedirect
from decouple import config
from rest_framework.authtoken.models import Token
from profile_app.models import Profile


class RegistrationView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username_profile = request.data['username'] 
        request.data['username'] = generate_username(request)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = generate_response_data(token, saved_account, username_profile)
            generate_profile(request, saved_account, username_profile) 
            send_confirmation_email(saved_account, request.data['first_name'], request.data['last_name'])
            return Response({"message": "Bitte überprüfe deine E-Mails, um deinen Account zu aktivieren.", "data": data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccountView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponseRedirect(config('DOMAIN_REDIRECT'))
            return Response({"error": "Ungültiger oder abgelaufener Token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Aktivierungsfehler."}, status=status.HTTP_400_BAD_REQUEST)


def generate_username(request):
    username = request.data.get('username', '') 
    if ' ' in username:
            username = username.replace(' ', '_')
    return username.lower()

def generate_response_data(token, saved_account, username_profile):
    data = {
                'token': token.key,
                'username': username_profile,
                'email': saved_account.email,
                "user_id": saved_account.pk
            }
    return data

def send_confirmation_email(user, first_name, last_name):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    full_link = f"{config('ROOT-DOMAIN')}{activation_link}"
    subject = "Bestätige deinen Videoflix-Account"
    html_message = generate_email(first_name, last_name, full_link)
    plain_message = f"Hallo {user.username}, bitte aktiviere deinen Account hier: {full_link}"
    send_mail(subject, plain_message, config('EMAIL_USER'), [user.email], html_message=html_message)

def generate_email(first_name, last_name, full_link):
    html_message = f"""
    <p>Hallo {first_name} {last_name},</p>
    <p>Bitte aktiviere deinen Videoflix-Account, indem du auf den folgenden Link klickst:</p>
    <p><a href="{full_link}">Account aktivieren</a></p>
    <p>Vielen Dank, dass du dich für Videoflix entschieden hast!</p>
    """
    return html_message

def generate_profile(request, saved_account, username_profile):
    Profile.objects.create(
        user=saved_account.pk,
        username=username_profile,
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=saved_account.email,
    )