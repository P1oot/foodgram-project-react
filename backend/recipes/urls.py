from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import TagViewSet, RecipeViewSet

router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
