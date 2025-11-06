from django.contrib import admin
from .models import MenuItem, Reservation, ContactMessage, SiteSetting, Testimonial, AboutSection


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


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
	list_display = ("address", "phone", "email", "newsletter_enabled")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("name", "role", "is_active", "order")
	list_editable = ("is_active", "order")
	search_fields = ("name", "role", "quote")
	list_filter = ("is_active",)


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
	list_display = ("title",)
