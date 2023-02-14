from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='me')
    def recent_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)