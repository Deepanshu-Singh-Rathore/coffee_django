from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_authtoken_views
from .views import (
    MenuItemViewSet, CategoryViewSet, PostViewSet,
    HeroSlideViewSet, FeatureViewSet, PromoViewSet,
    ContactMessageViewSet, StudentViewSet,
    ProductListProxy, ProductDetailProxy, ProductRandomProxy,
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'hero-slides', HeroSlideViewSet, basename='heroslide')
router.register(r'features', FeatureViewSet, basename='feature')
router.register(r'promos', PromoViewSet, basename='promo')
router.register(r'contact-messages', ContactMessageViewSet, basename='contactmessage')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', drf_authtoken_views.obtain_auth_token, name='api_token_auth'),
    # Product proxy endpoints (Fake Store API)
    path('products/', ProductListProxy.as_view(), name='product-list-proxy'),
    path('products/<int:product_id>/', ProductDetailProxy.as_view(), name='product-detail-proxy'),
    path('products/random/', ProductRandomProxy.as_view(), name='product-random-proxy'),
]
