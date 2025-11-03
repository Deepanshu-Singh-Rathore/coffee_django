from django.contrib import admin
from .models import MenuItem, Reservation, ContactMessage


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "is_featured", "home_order")
	list_editable = ("is_featured", "home_order")
	search_fields = ("name", "description")
	list_filter = ("is_featured",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "phone", "date", "time", "number_of_people", "created_at")
	list_filter = ("date",)
	search_fields = ("name", "email", "phone")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "created_at")
	search_fields = ("name", "email")
