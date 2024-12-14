from rest_framework import serializers

from apps.profiles.serializers import ProfileSerializer
from apps.shop.serializers import ProductSerializer


class ReviewSerializer(serializers.Serializer):
    user = ProfileSerializer()
    product = ProductSerializer()
    rating = serializers.IntegerField()
    text = serializers.CharField()


class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)
