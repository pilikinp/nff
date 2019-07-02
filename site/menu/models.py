from django.db import models
# from imageapp.models import ImageMeal


class Category(models.Model):
    '''Категории блюд'''
    title = models.CharField(
        max_length=64,
        null=True,
        default='Без категории'
    )

    image = models.ImageField(
        upload_to='images/categories/',
        null=True,
        blank=True
    )


class Product(models.Model):
    '''Продукты'''
    title = models.CharField(
        max_length=64,
        null=False
    )

    image = models.ImageField(
        upload_to='images/products/',
        null=True,
        blank=True
    )

    energy = models.IntegerField(
        null=False
    )

    protein = models.IntegerField(
        null=False
    )

    fat = models.IntegerField(
        null=False
    )

    carbohydrate = models.IntegerField(
        null=False
    )


class Ingredient(models.Model):
    '''Ингредиент блюда'''
    product = models.ForeignKey(
        'menu.Product',
        on_delete=models.CASCADE
    )

    weight = models.IntegerField(
        null=False
    )


class Meal(models.Model):
    '''Блюдо'''
    title = models.CharField(
        max_length=128
    )

    category = models.ForeignKey(
        'menu.Category',
        on_delete=models.CASCADE
    )

    ingredients = models.ManyToManyField(
        'menu.Ingredient'
    )

    recipe = models.TextField(
        null=False
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False
    )

    snippet = models.CharField(
        max_length=125,
        null=True,
        blank=True
    )

    # image = models.ForeignKey(
    #     ImageMeal,
    #     on_delete=models.PROTECT,
    #     null=True,
    #     blank=True,
    # )

    image = models.ImageField(
        upload_to='images/meals/',
        null=True,
        blank=True
    )

    def get_weight(self):
        return sum(map(lambda x: x.weight, self.get_ingredients()))

    def get_ingredients(self):
        return [
            {
                'title': ingredient.product.title,
                'weight': ingredient.weight
            }
            for ingredient in self.ingredients.all()
        ]
