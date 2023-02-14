# Generated by Django 2.2.19 on 2023-02-13 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230213_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.Ingredient', verbose_name='Ингредиент'),
        ),
    ]
