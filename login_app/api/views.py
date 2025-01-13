from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from profile_app.models import Profile

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
                'username': profile.username,
                'email': profile.email,
                "user_id": user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


