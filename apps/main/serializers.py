from rest_framework import serializers

from apps.main.models import Order, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class OrderSerializer(serializers.ModelSerializer):
    tags_info = TagSerializer(many=True, read_only=True, source='tags')

    class Meta:
        model = Order
        fields = ['id', 'status', 'tags', 'tags_info']
        extra_kwargs = {'tags': {'write_only': True}}

