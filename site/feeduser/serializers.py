from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile

from feeduser.models import FeedUser, ProducerProfile, ConsumerProfile
from menu.serializers import MealSerializer


class UserSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        avatar = validated_data.pop('avatar')
        user_data = validated_data
        if instance.username != user_data.get('username'):
            instance.username = user_data.get('username')
        instance.first_name = user_data.get('first_name')
        instance.last_name = user_data.get('last_name')
        instance.location = user_data.get('location')
        instance.email = user_data.get('email')
        instance.avatar = avatar
        instance.save()
        return instance

    def to_internal_value(self, data):
        if not isinstance(data.get('avatar', None), InMemoryUploadedFile):
            data['avatar'] = self.instance.avatar
        return data

    class Meta:
        model = FeedUser
        validators = []
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'location',
            'avatar',
            'email'
        ]

    def get_avatar(self, obj):
        return obj.url


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=FeedUser.objects.all())]
    )
    password = serializers.CharField(min_length=3, style={'input_type': 'password'})

    def to_internal_value(self, data):
        if not isinstance(data.get('avatar', None), InMemoryUploadedFile):
            self.avatar = serializers.ImageField(validators=[])
        return data

    def create(self, validated_data):
        # print('here!', validated_data)
        user = FeedUser.objects.create_user(username=validated_data.get('username'),
                                            password=validated_data.get('password'),
                                            first_name=validated_data.get('first_name'),
                                            last_name=validated_data.get('last_name'),
                                            email=validated_data.get('email'),
                                            avatar=validated_data.get('avatar', None))
        return user

    class Meta:
        model = FeedUser
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'avatar',
            'email'
        ]


class ChefSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProducerProfile
        validators = []
        fields = [
            'id',
            'user',
        ]


class ProducerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menu = MealSerializer(many=True)

    def update(self, instance, validated_data):
        print('here>>')
        user_data = validated_data.get('user')
        if instance.user.username != user_data.get('username'):
            instance.user.username = user_data.get('username')
        instance.user.first_name = user_data.get('first_name')
        instance.user.last_name = user_data.get('last_name')
        instance.user.location = user_data.get('location')

        instance.user.email = user_data.get('email')

        instance.phone = validated_data.get('phone')
        instance.snippet = validated_data.get('snippet')
        instance.save()
        return instance

    class Meta:
        model = ProducerProfile
        validators = []
        fields = [
            'id',
            'user',
            'phone',
            'snippet',
            'menu',
        ]


class UpdateProducerSerializer(serializers.ModelSerializer):
    # menu = MealSerializer(many=True)

    class Meta:
        model = ProducerProfile
        fields = [
            'id',
            'phone',
            'snippet',
            # 'menu'
        ]

    def update(self, instance, validated_data):
        print('!!!!!!!!!!!!!', instance)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.snippet = validated_data.get('snippet', instance.snippet)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance


class UpdateConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerProfile
        fields = [
            'id',
            'phone',
            'snippet',
        ]

    def update(self, instance, validated_data):
        print('!!!!!!!!!!!!!', instance)
        print('!!!!!!!!!!!!!', validated_data)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.snippet = validated_data.get('snippet', instance.snippet)
        instance.save()
        return instance


class ConsumerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ConsumerProfile
        fields = [
            'id',
            'user',
            'phone',
            'snippet',
        ]
