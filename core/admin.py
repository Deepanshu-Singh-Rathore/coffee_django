from django.contrib import admin
from .models import MenuItem, Reservation, ContactMessage

admin.site.register(MenuItem)
admin.site.register(Reservation)
admin.site.register(ContactMessage)
