from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import TagViewSet, RecipeViewSet, IngredientViewSet

router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls))
]
