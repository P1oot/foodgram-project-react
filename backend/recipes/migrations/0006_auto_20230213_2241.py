# Generated by Django 2.2.19 on 2023-02-13 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230213_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]