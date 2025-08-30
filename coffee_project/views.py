from django.shortcuts import render


def HomePage(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def service(request):
    return render(request, "service.html")


def menu(request):
    return render(request, "menu.html")


def reservation(request):
    return render(request, "reservation.html")


def testimonial(request):
    return render(request, "testimonial.html")


def contact(request):
    return render(request, "contact.html")