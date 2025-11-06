from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from core.models import MenuItem, ContactMessage, Reservation
from core.models import Testimonial as TestimonialModel, AboutSection as AboutSectionModel
from hero.models import HeroSlide
from feature.models import Feature as FeatureModel
from promo.models import Promo as PromoModel
from django.http import JsonResponse, HttpResponseBadRequest
import json
import requests
from core.forms import MenuItemForm, ContactForm, ReservationForm
from blog.models import Post
from django.db.models import Q


def HomePage(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    features = FeatureModel.objects.filter(is_active=True).order_by('order')
    promos = PromoModel.objects.filter(is_active=True).order_by('order')
    featured_menu = MenuItem.objects.filter(is_featured=True).order_by('home_order', 'name')[:6]
    latest_posts = Post.objects.filter(is_published=True)[:3]
    return render(request, "index.html", {
        "hero_slides": hero_slides,
        "features": features,
        "promos": promos,
        "featured_menu": featured_menu,
        "latest_posts": latest_posts,
    })


def about(request):
    about_section = AboutSectionModel.objects.first()
    return render(request, "about.html", {"about": about_section})


def service(request):
    features = FeatureModel.objects.filter(is_active=True).order_by('order')
    return render(request, "service.html", {"features": features})


def menu_list(request):
    items = MenuItem.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))
    sort = request.GET.get('sort', 'name')
    if sort == 'price':
        items = items.order_by('price', 'name')
    else:
        sort = 'name'
        items = items.order_by('name')
    return render(request, "menu.html", {"items": items, "active_sort": sort, "query": q})

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
    success = False
    form = ReservationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        success = True
        form = ReservationForm()  # reset form after successful save
    return render(request, "reservation.html", {"form": form, "success": success})


def testimonial(request):
    testimonials = TestimonialModel.objects.filter(is_active=True)
    return render(request, "testimonial.html", {"testimonials": testimonials})


def contact(request):
    success = False
    email_error = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Send an email (SMTP if configured, console in dev)
            subject = f"Contact message from {msg.name}"
            context = {
                "name": msg.name,
                "email": msg.email,
                "message": msg.message,
                "sent_at": msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            text_body = render_to_string('email/contact_message.txt', context)
            html_body = render_to_string('email/contact_message.html', context)
            try:
                email = EmailMultiAlternatives(
                    subject,
                    text_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL_TO],
                )
                email.attach_alternative(html_body, 'text/html')
                email.send()
                success = True
            except Exception as e:
                # Log error details in development for easier diagnosis
                try:
                    if settings.DEBUG:
                        print("Email send error:", e)
                except Exception:
                    pass
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