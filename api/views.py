from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import MenuItem, ContactMessage
from blog.models import Category, Post
from hero.models import HeroSlide
from feature.models import Feature
from promo.models import Promo
from .serializers import (
    MenuItemSerializer, ContactMessageSerializer,
    CategorySerializer, PostSerializer,
    HeroSlideSerializer, FeatureSerializer, PromoSerializer,
)


class ReadOnlyOrAdmin(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class MenuItemViewSet(ReadOnlyOrAdmin):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer


class CategoryViewSet(ReadOnlyOrAdmin):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class PostViewSet(ReadOnlyOrAdmin):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class HeroSlideViewSet(ReadOnlyOrAdmin):
    queryset = HeroSlide.objects.filter(is_active=True).order_by('created_at')
    serializer_class = HeroSlideSerializer


class FeatureViewSet(ReadOnlyOrAdmin):
    queryset = Feature.objects.filter(is_active=True).order_by('order', 'id')
    serializer_class = FeatureSerializer


class PromoViewSet(ReadOnlyOrAdmin):
    queryset = Promo.objects.filter(is_active=True).order_by('order', 'id')
    serializer_class = PromoSerializer


class ContactMessageViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
