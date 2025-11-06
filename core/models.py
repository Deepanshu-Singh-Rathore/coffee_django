from django.db import models

class MenuItem(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	home_order = models.PositiveIntegerField(default=0, help_text="Order for homepage featured list")

	def __str__(self):
		return self.name

class Reservation(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	date = models.DateField()
	time = models.TimeField()
	number_of_people = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Reservation for {self.name} on {self.date} at {self.time}"

class ContactMessage(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message from {self.name} ({self.email})"


class SiteSetting(models.Model):
	address = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=50, blank=True)
	email = models.EmailField(blank=True)
	open_hours_weekday = models.CharField(max_length=120, blank=True, default="8.00 AM - 8.00 PM")
	open_hours_weekend = models.CharField(max_length=120, blank=True, default="2.00 PM - 8.00 PM")
	facebook_url = models.URLField(blank=True)
	twitter_url = models.URLField(blank=True)
	instagram_url = models.URLField(blank=True)
	linkedin_url = models.URLField(blank=True)
	newsletter_enabled = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Site Setting"
		verbose_name_plural = "Site Settings"

	def __str__(self):
		return "Site Settings"


class Testimonial(models.Model):
	name = models.CharField(max_length=120)
	role = models.CharField(max_length=120, blank=True)
	quote = models.TextField()
	photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
	is_active = models.BooleanField(default=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', 'id']

	def __str__(self):
		return self.name


class AboutSection(models.Model):
	title = models.CharField(max_length=200, default="About Us")
	subtitle = models.CharField(max_length=250, blank=True)
	content_left_title = models.CharField(max_length=150, default="Our Story")
	content_left_subtitle = models.CharField(max_length=250, blank=True)
	content_left_body = models.TextField(blank=True)
	content_right_title = models.CharField(max_length=150, default="Our Vision")
	content_right_body = models.TextField(blank=True)
	image = models.ImageField(upload_to='about/', blank=True, null=True)

	def __str__(self):
		return self.title
