from django.shortcuts import render, redirect
from core.models import MenuItem
from core.forms import MenuItemForm


def HomePage(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def service(request):
    return render(request, "service.html")


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
    return render(request, "contact.html")