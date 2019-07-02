from django.contrib import admin

from menu.models import Meal


# Register your models here.

@admin.register(Meal)
class Mealadmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'recipe',
        'price',
        'snippet',
    ]
