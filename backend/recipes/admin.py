from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngredientAmount, Favorites


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientsInline]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites)
