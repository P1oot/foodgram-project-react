from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
