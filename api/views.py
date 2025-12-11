from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.cache import cache
import requests
import random
from core.models import MenuItem, ContactMessage, Coffee
from blog.models import Category, Post
from hero.models import HeroSlide
from feature.models import Feature
from promo.models import Promo
from .serializers import (
    MenuItemSerializer, ContactMessageSerializer,
    CategorySerializer, PostSerializer,
    HeroSlideSerializer, FeatureSerializer, PromoSerializer, CoffeeSerializer,
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


class CoffeeViewSet(ReadOnlyOrAdmin):
    queryset = Coffee.objects.all().order_by('name')
    serializer_class = CoffeeSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_roast(self, request):
        roast = request.GET.get('roast')
        if roast:
            qs = self.get_queryset().filter(roast_type=roast)
        else:
            qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_origin(self, request):
        origin = request.GET.get('origin')
        if origin:
            qs = self.get_queryset().filter(origin__icontains=origin)
        else:
            qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


FAKESTORE_BASE_URL = "https://fakestoreapi.com"


class ProductListProxy(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        category = request.GET.get("category")
        cache_key = f"fakestore_products_{category or 'all'}"
        data = cache.get(cache_key)
        if data is None:
            try:
                if category:
                    url = f"{FAKESTORE_BASE_URL}/products/category/{category}"
                else:
                    url = f"{FAKESTORE_BASE_URL}/products"
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                cache.set(cache_key, data, 300)  # 5 minutes
            except requests.RequestException as e:
                status_code = getattr(getattr(e, 'response', None), 'status_code', 502) or 502
                return Response({"detail": "Upstream products API error."}, status=status_code)
        return Response(data)


class ProductDetailProxy(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id: int):
        cache_key = f"fakestore_product_{product_id}"
        data = cache.get(cache_key)
        if data is None:
            try:
                url = f"{FAKESTORE_BASE_URL}/products/{product_id}"
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                cache.set(cache_key, data, 300)
            except requests.RequestException as e:
                status_code = getattr(getattr(e, 'response', None), 'status_code', 502) or 502
                return Response({"detail": "Upstream products API error."}, status=status_code)
        return Response(data)


class ProductRandomProxy(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cache_key = "fakestore_products_all"
        data = cache.get(cache_key)
        if data is None:
            try:
                resp = requests.get(f"{FAKESTORE_BASE_URL}/products", timeout=10)
                resp.raise_for_status()
                data = resp.json()
                cache.set(cache_key, data, 300)
            except requests.RequestException:
                return Response({"detail": "Upstream products API error."}, status=502)
        if not data:
            return Response({"detail": "No products available."}, status=502)
        return Response(random.choice(data))
