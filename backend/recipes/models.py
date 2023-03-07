from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField('Адрес', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        help_text='Название продукта',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Размерность',
        help_text='В чем измеряется',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиет'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        verbose_name='Названеие',
        help_text='Название блюда',
        max_length=200,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
        help_text='Тег',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientAmount',
        verbose_name='Ингредиент',
        help_text='Ингредиент',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='мин',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Опишите блюдо и способ приготовления',
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/images/',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient',
    )
    amount = models.FloatField(
        verbose_name='Количесво',
        help_text='Количество продукта',
        max_length=5,
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredients', 'recipe'],
                name='unique_ingredients_recipe'
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Любимые рецепты',
        related_name='is_favorite',
        on_delete=models.CASCADE,
    )
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        ordering = ['-date_add']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]


class ShoppingCarts(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Владелец корзины',
        related_name='cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты в корзине',
        related_name='in_cart',
        on_delete=models.CASCADE,
    )
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
        ordering = ['-date_add']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_in_cart'
            )
        ]
