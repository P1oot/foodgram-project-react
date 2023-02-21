from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import User, Follow
from .serializers import (UserSerializer, SetPasswordSerializer,
                          SubscriptionSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(
        methods=('get',),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def recent_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post',],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(
                serializer.data.get("current_password")
            ):
                return Response(
                    {"current_password": ["Неверный пароль"]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        follow = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if follow.exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscription(self, request):
        user = request.user
        data = User.objects.filter(following__user=user)
        serializer = SubscriptionSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
