"""
URL configuration for coffee_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from coffee_project import views
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.menu_add, name='menu_add'),
    path('reservation/', views.reservation, name='reservation'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),
    # Blog
    path('blog/', blog_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_views.blog_detail, name='blog_detail'),
    # Simple JSON APIs
    path('api/menu/', views.api_menu, name='api_menu'),
    path('api/blog/', views.api_blog_posts, name='api_blog_posts'),
    path('api/contact/', views.api_contact_create, name='api_contact_create'),
    path('api-integration/', views.api_integration_page, name='api_integration'),
    # DRF v1 API
    path('api/v1/', include('api.urls')),
    # Coffee data page
    path('coffee/', views.coffeeData, name='coffee'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
