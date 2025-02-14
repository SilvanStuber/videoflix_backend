from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        username = self.validated_data['username']
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        if '@' in username:
            raise serializers.ValidationError({"detail": ["Kein @ im Username angeben."]})  
        if pw != repeated_pw:
            raise serializers.ValidationError({"detail": ["Das Passwort ist nicht gleich mit dem wiederholten Passwort."]})       
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"detail": ["Diese E-Mail-Adresse wird bereits verwendet."]})
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({"detail": ["Dieser Benutzername ist bereits vergeben."],})
        else:
            account = User(email=self.validated_data['email'], username=self.validated_data['username'], is_active=False)
            account.set_password(pw)
            account.save()
            return account

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    repeated_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate(self, data):
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        if password != repeated_password:
            raise serializers.ValidationError({"detail": "Die Passwörter stimmen nicht überein."})

        return data

class OldPasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({"detail": "Das alte Passwort ist falsch."})
        if data.get('password') != data.get('repeated_password'):
            raise serializers.ValidationError({"detail": "Die Passwörter stimmen nicht überein."})
        return data

    def update_password(self):
        """Setzt das neue Passwort für den Benutzer."""
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()

