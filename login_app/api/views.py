from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from profile_user_app.models import Profile

class CostomLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            profile = Profile.objects.get(user=user.pk)
            data = {
                'token': token.key,
                'user': user.id,
                'username': profile.username,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,   
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


