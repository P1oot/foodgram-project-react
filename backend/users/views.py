from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, SetPasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, url_path='me')
    def recent_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(methods=['post',], detail=False, url_path='set_password')
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("current_password")):
                return Response({"current_password": ["Неверный пароль"]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
