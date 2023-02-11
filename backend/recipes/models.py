from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200,unique=True)
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
        related_name='recipe',
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
        related_name='recipe',
        verbose_name='Тег',
        help_text='Тег',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe',
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
    # image = models.ImageField(
    #     verbose_name='Картинка',
    #     upload_to='recipe/',
    #     blank=True
    # )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.FloatField(
        verbose_name='Количесво',
        help_text='Количество продукта',
        max_length=5,
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        unique_together = ['ingredient', 'recipe']
