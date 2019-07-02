from django.core.management.base import BaseCommand
import random

from menu.models import Product, Ingredient, Category, Meal

product_img = 'images/products/product.jpg'

meal_img = 'images/meals/meal.jpg'

CATEGORIES = ['First Category', 'Second Category', 'Third Category']
PRODUCTS = [
    {
        'title': f'product_{i}',
        'energy': random.randint(100, 200),
        'protein': random.randint(100, 200),
        'fat': random.randint(100, 200),
        'carbohydrate': random.randint(100, 200),
        # 'image': product_img
    } for i in range(1, 51)
]

MEAL_TITLES = [f'Meal_{i}' for i in range(1, 21)]
MEAL_RECIPE = 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus'


class Command(BaseCommand):
    help = '''
    fill test db
    '''

    def add_arguments(self, parser):
        parser.add_argument('-a')

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Ingredient.objects.all().delete()
        Meal.objects.all().delete()

        # создаем продукты
        products_gen = (Product(**item) for item in PRODUCTS)
        Product.objects.bulk_create(products_gen)

        categories_gen = (Category(title=item) for item in CATEGORIES)
        Category.objects.bulk_create(categories_gen)

        categories = Category.objects.all()
        products = Product.objects.all()

        # создаем ингредиенты
        ingredients_gen = (Ingredient(
            product=random.choice(products),
            weight=random.randint(100, 500)
        ) for _ in range(20))
        Ingredient.objects.bulk_create(ingredients_gen)

        ingredients = Ingredient.objects.all()

        # создаем блюда
        meals_gen_ = (
            Meal(**{
                'title': random.choice(MEAL_TITLES),
                'category': random.choice(categories),
                'recipe': MEAL_RECIPE,
                'price': random.randint(150, 350),
                'image': meal_img
            }) for _ in range(10)
        )

        Meal.objects.bulk_create(meals_gen_)

        meals = Meal.objects.all()
        for meal in meals:
            meal.ingredients.add(*[random.choice(ingredients) for _ in range(random.randint(2, 5))])
