from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile

from menu.models import Meal, Ingredient, Product, Category
from feeduser.models import ProducerProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'energy',
            'protein',
            'fat',
            'carbohydrate',
            'image'
        ]

    def to_internal_value(self, data):
        if not isinstance(data.get('image', None), InMemoryUploadedFile):
            data['image'] = self.instance.image
        return data

    def get_image(self, obj):
        return obj.url


class IngredientSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'product',
            'weight'
        ]


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerProfile
        validators = []
        fields = [
            'id',
        ]


class MealSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    category = CategorySerializer()
    producerprofile_set = ChefSerializer(many=True)

    class Meta:
        model = Meal
        fields = [
            'id',
            'title',
            'category',
            'ingredients',
            'recipe',
            'price',
            'snippet',
            'image',
            'producerprofile_set'
        ]

    def to_internal_value(self, data):
        if not isinstance(data.get('image', None), InMemoryUploadedFile):
            data['image'] = self.instance.image
        return data

    def get_image(self, obj):
        return obj.url

    # def get_producerprofile_set(self, obj):
    #     return obj.producerprofile_set.all()
