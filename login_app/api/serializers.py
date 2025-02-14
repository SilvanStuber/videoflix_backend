from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CustomLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get('username_or_email')
        password = data.get('password')
        if not username_or_email or not password:
            raise serializers.ValidationError({"detail": "Benutzername oder E-Mail und Passwort sind erforderlich."})  
        user = None
        if '@' in username_or_email:    
           user = loginWithEmail(username_or_email, password)
        else:
           user = loginWithUsername(username_or_email, password)
        if user is None:
            raise serializers.ValidationError({"detail": "Ungültige Logindaten oder der Benutzer ist deaktiviert. Bitte überprüfe deine E-Mails und aktiviere dein Konto."})
        data['user'] = user
        return data
    
def loginWithUsername(username_or_email, password):
    try:
        username = generate_username_login(username_or_email)
        user = authenticate(username=username, password=password)
    except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Ungültige Logindaten oder der Benutzer ist deaktiviert. Bitte überprüfe deine E-Mails und aktiviere dein Konto."})    
    return user

def loginWithEmail(username_or_email, password):
        try:
            user_instance = User.objects.get(email=username_or_email)
            user = authenticate(username=user_instance.username, password=password)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Ungültige Logindaten oder der Benutzer ist deaktiviert. Bitte überprüfe deine E-Mails und aktiviere dein Konto."})
        return user

def generate_username_login(username):
    if ' ' in username:
        username = username.replace(' ', '_')
    return username.lower()