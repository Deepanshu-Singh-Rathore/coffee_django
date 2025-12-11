#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin user
username = "admin"
email = "admin@coffeeproject.com"
password = "admin123"

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"⚠ User '{username}' already exists!")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✓ Password updated for '{username}'")
else:
    user = User.objects.create_superuser(username, email, password)
    print(f"✓ Superuser '{username}' created successfully!")

print(f"\n--- Admin Login Credentials ---")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Email: {email}")
print(f"\nAdmin URL: http://127.0.0.1:8002/admin/")
