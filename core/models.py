from django.db import models

class MenuItem(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

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
