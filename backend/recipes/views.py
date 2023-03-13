from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.serializers import ShortRecipeSerializer

from .filters import AuthorAndTagFilter
from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCarts, Tag)
from .paginataion import PageLimitPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorAndTagFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = Favorites.objects.filter(user=user, recipe=recipe)
        if favorites.exists():
            if request.method == 'POST':
                return Response(
                    {'errors': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепта нет в избранном'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        cart = ShoppingCarts.objects.filter(user=user, recipe=recipe)
        if cart.exists():
            if request.method == 'POST':
                return Response(
                    {'errors': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            ShoppingCarts.objects.create(user=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепта нет в корзине'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['get', ], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__in_cart__user=user
        ).values_list('ingredients__name',
                      'ingredients__measurement_unit', 'amount')
        cart_str = 'Список покупок:\n\n'
        cart = {}
        for ing in ingredients:
            name = ing[0]
            if name not in cart:
                cart[name] = {
                    'measurement_unit': ing[1],
                    'amount': ing[2]
                }
            else:
                cart[name]['amount'] += ing[2]
        for ing in cart:
            amount = cart[ing]['amount']
            unit = cart[ing]['measurement_unit']
            cart_str += f'{ing}: {amount} {unit}\n'
        filename = f'{user}_shopping_cart.txt'
        response = HttpResponse(cart_str, content_type='text/plain')
        response['Content-Disposition'] = ('attachment; filename={0}'
                                           .format(filename))
        return response
