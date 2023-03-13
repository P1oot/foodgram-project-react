from django.contrib import admin

from .models import (Favorites, Ingredient, IngredientAmount, Recipe,
                     ShoppingCarts, Tag)


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientsInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(IngredientAmount, Favorites, ShoppingCarts)
class SimpleAdmin(admin.ModelAdmin):
    pass
