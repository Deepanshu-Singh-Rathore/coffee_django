from rest_framework import serializers
from core.models import MenuItem, ContactMessage
from blog.models import Category, Post
from hero.models import HeroSlide
from feature.models import Feature
from promo.models import Promo


class ImageUrlSerializerMixin:
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if getattr(obj, 'image', None):
            try:
                url = obj.image.url
                return request.build_absolute_uri(url) if request else url
            except Exception:
                return None
        if getattr(obj, 'background_image', None):
            try:
                url = obj.background_image.url
                return request.build_absolute_uri(url) if request else url
            except Exception:
                return None
        return None


class MenuItemSerializer(ImageUrlSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'image_url']
        read_only_fields = ['id', 'image_url']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class PostSerializer(ImageUrlSerializerMixin, serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source='category')

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'image', 'image_url',
            'category', 'category_id', 'is_published', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'image_url', 'created_at']


class HeroSlideSerializer(ImageUrlSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = HeroSlide
        fields = ['id', 'title', 'subtitle', 'background_image', 'image_url', 'is_active', 'created_at']
        read_only_fields = ['id', 'image_url', 'created_at']


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description', 'icon_class', 'is_active', 'order']
        read_only_fields = ['id']


class PromoSerializer(ImageUrlSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'title', 'description', 'image', 'image_url', 'button_text', 'button_url', 'is_active', 'order']
        read_only_fields = ['id', 'image_url']
