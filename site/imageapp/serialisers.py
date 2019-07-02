from rest_framework import serializers

from imageapp.models import ImageMeal


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageMeal
        fields = (
            'url',
        )
