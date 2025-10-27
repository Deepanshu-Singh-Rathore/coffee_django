from django.contrib import admin
from .models import Promo

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
