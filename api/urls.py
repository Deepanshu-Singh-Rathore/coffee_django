from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_authtoken_views
from .views import (
    MenuItemViewSet, CategoryViewSet, PostViewSet,
    HeroSlideViewSet, FeatureViewSet, PromoViewSet,
    ContactMessageViewSet,
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'hero-slides', HeroSlideViewSet, basename='heroslide')
router.register(r'features', FeatureViewSet, basename='feature')
router.register(r'promos', PromoViewSet, basename='promo')
router.register(r'contact-messages', ContactMessageViewSet, basename='contactmessage')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', drf_authtoken_views.obtain_auth_token, name='api_token_auth'),
]
