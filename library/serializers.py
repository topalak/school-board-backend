from rest_framework import serializers
from .models import Category, Book


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'tier_level',
                  'category', 'uploaded_by', 'created_at']
        read_only_fields = ['uploaded_by', 'created_at']