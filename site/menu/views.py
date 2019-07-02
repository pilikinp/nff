from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ModelViewSet
from feeduser.models import ProducerProfile
from menu.models import Meal, Product, Category, Ingredient
from menu.serializers import MealSerializer, ProductSerializer, CategorySerializer
from imageapp.models import ImageMeal

import json


class PaginateBy(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_size_query_param = 'page_size'


class MealsList(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    pagination_class = PaginateBy

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = Meal.objects.get(pk=pk)
        if instance:
            serializer = MealSerializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if 'ids' in request.GET:
            ids = list(map(lambda x: int(x), request.GET['ids'].split(',')))
            queryset = Meal.objects.filter(pk__in=ids)
        else:
            queryset = Meal.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MealSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MealSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        # print(json.loads(request.data.get('newMeal')))

        if request.data.get('newMeal'):
            data_meal = json.loads(request.data.get('newMeal'))
            data_meal.update({'image': request.data.get('file')})

            producer = ProducerProfile.objects.filter(user__id=data_meal.get('user_id'))[0]
            title = data_meal.get('title')
            category = Category.objects.get(pk=data_meal.get('category'))
            price = data_meal.get('price')
            snippet = data_meal.get('snippet')
            recipe = data_meal.get('recipe')
            ingredients_gen = (Ingredient(product=Product.objects.get(id=p['product_id']), weight=p['weight']) for p in
                               data_meal.get('ingredients'))
            Ingredient.objects.bulk_create(ingredients_gen)
            meal = Meal.objects.create(
                title=title,
                category=category,
                price=price,
                recipe=recipe,
                snippet=snippet,
                image=request.data.get('file')
            )
            meal.save()
            ingredients = Ingredient.objects.all().order_by('-id')[:len(data_meal.get('ingredients'))]
            meal.ingredients.add(*ingredients)
            if producer:
                producer.menu.add(meal)

            return Response({'res': 'OK'}, status=HTTP_200_OK)
        else:
            print(request.data)
            meal = Meal.objects.get(id=request.data.get('meal'))
            producer = ProducerProfile.objects.get(user__id=request.data.get('consumer'))
            if producer.menu.filter(id=meal.id):
                return Response({'res': 'Уже добавлено'}, status=HTTP_200_OK)
            producer.menu.add(meal)
            return Response({'res': 'OK'}, status=HTTP_200_OK)


class ProductsList(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        # page = self.paginate_queryset(self.queryset)
        # if page is not None:
        #     serializer = ProductSerializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = ProductSerializer(Product.objects.all(), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        print(json.loads(request.data.get('newProduct')))

        data_product = json.loads(request.data.get('newProduct'))
        data_product.update({'image': request.data.get('file')})

        product = Product.objects.create(
            title=data_product.get('title'),
            image=data_product.get('image'),
            energy=data_product.get('energy'),
            protein=data_product.get('protein'),
            fat=data_product.get('fat'),
            carbohydrate=data_product.get('carbohydrate')
        )
        product.save()
        serializer = ProductSerializer(product)
        return Response({'res': 'OK', 'product': serializer.data}, status=HTTP_200_OK)


class CategoriesList(ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = CategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
