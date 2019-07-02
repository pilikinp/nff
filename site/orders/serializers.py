from rest_framework import serializers

from orders.models import OrderItem
from menu.serializers import MealSerializer  # TODO написать отдельный сериализатор с одним полем id
from feeduser.serializers import ChefSerializer, UserSerializer


class ListOrderSerializer(serializers.ModelSerializer):
    consumer = UserSerializer()
    chef = ChefSerializer()
    meal = MealSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'consumer',
            'chef',
            'meal',
            'quantity',
            'status',
            'item_price'
        ]

    def get_item_price(self, obj):
        return obj.item_price


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'consumer',
            'chef',
            'meal',
            'quantity',
            'status'
        ]

    def create(self, validated_data):
        print('>>>', validated_data)
        chef = validated_data.get('chef')
        consumer = validated_data.get('consumer')
        meal = validated_data.get('meal')
        quantity = validated_data.get('quantity')

        item = OrderItem(
            consumer=consumer,
            chef=chef,
            meal=meal,
            quantity=quantity
        )
        item.save()
        return item

    def update(self, instance, validated_data):
        print('>>', validated_data)
        instance.chef = validated_data.get('chef')
        instance.consumer = validated_data.get('consumer')
        instance.meal = validated_data.get('meal')
        instance.quantity = validated_data.get('quantity')
        instance.status = validated_data.get('status')
        instance.save()
        return instance
