#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_project.settings')
django.setup()

from core.models import ContactMessage

messages = ContactMessage.objects.all().order_by('-created_at')
print(f"\n{'='*60}")
print(f"CONTACT MESSAGES ({messages.count()} total)")
print(f"{'='*60}\n")

if messages.exists():
    for msg in messages:
        print(f"From: {msg.name} <{msg.email}>")
        print(f"Date: {msg.created_at}")
        print(f"Message: {msg.message}")
        print("-" * 60)
else:
    print("No contact messages yet.")
    print("\nTo submit a contact message:")
    print("1. Visit http://127.0.0.1:8002/contact/")
    print("2. Fill out the form and submit")
    print("3. The message will appear here and be sent to: deepanshu052005@gmail.com")
