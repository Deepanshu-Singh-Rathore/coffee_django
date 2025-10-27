from django.shortcuts import render, redirect
from django.core.mail import send_mail
from core.models import MenuItem, ContactMessage
from hero.models import HeroSlide
from feature.models import Feature as FeatureModel
from promo.models import Promo as PromoModel
from django.http import JsonResponse, HttpResponseBadRequest
import json
import requests
from core.forms import MenuItemForm, ContactForm


def HomePage(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    features = FeatureModel.objects.filter(is_active=True).order_by('order')
    promos = PromoModel.objects.filter(is_active=True).order_by('order')
    return render(request, "index.html", {
        "hero_slides": hero_slides,
        "features": features,
        "promos": promos,
    })


def about(request):
    return render(request, "about.html")


def service(request):
    features = FeatureModel.objects.filter(is_active=True).order_by('order')
    return render(request, "service.html", {"features": features})


def menu_list(request):
    items = MenuItem.objects.all().order_by('name')
    return render(request, "menu.html", {"items": items})

def menu_add(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("menu_list")
    else:
        form = MenuItemForm()
    return render(request, "menu_add.html", {"form": form})


def reservation(request):
    return render(request, "reservation.html")


def testimonial(request):
    return render(request, "testimonial.html")


def contact(request):
    success = False
    email_error = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Send an email (development: console backend)
            subject = f"Contact message from {msg.name}"
            body = f"Name: {msg.name}\nEmail: {msg.email}\n\nMessage:\n{msg.message}"
            try:
                send_mail(subject, body, None, ["info@example.com"])  # console in dev
                success = True
            except Exception as e:
                email_error = "Sorry, it seems our mail server is not responding. Please try again later."
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form, "success": success, "email_error": email_error})

# ---------- Simple JSON API endpoints ----------

def api_menu(request):
    data = [
        {
            "id": i.id,
            "name": i.name,
            "description": i.description,
            "price": float(i.price),
            "image_url": i.image.url if i.image else None,
        }
        for i in MenuItem.objects.all().order_by('name')
    ]
    return JsonResponse(data, safe=False)

def api_blog_posts(request):
    from blog.models import Post
    qs = Post.objects.filter(is_published=True)
    category = request.GET.get('category')
    if category:
        qs = qs.filter(category__slug=category)
    data = [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "category": p.category.name,
            "created_at": p.created_at.isoformat(),
            "image_url": p.image.url if p.image else None,
        }
        for p in qs
    ]
    return JsonResponse(data, safe=False)

def api_contact_create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    form = ContactForm(payload)
    if form.is_valid():
        msg = form.save()
        return JsonResponse({"status": "ok", "id": msg.id})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


def api_integration_page(request):
    third_party = None
    error = None
    try:
        r = requests.get('https://catfact.ninja/fact', timeout=5)
        if r.ok:
            third_party = r.json()
        else:
            error = f"API error: {r.status_code}"
    except Exception as e:
        error = str(e)
    return render(request, 'api_integration.html', {"third_party": third_party, "error": error})