from menu.views import MealsList
from django.urls import path

app_name = 'menu'

urlpatterns = [
    path('meals', MealsList.as_view({'get': 'list'}), name='meals_list'),
]