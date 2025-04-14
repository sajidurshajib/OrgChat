from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, RoleSerializer
from .models import Role

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UpdateOwnRoleView(generics.RetrieveUpdateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Role.objects.get(user=self.request.user)