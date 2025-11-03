from django import forms
from .models import MenuItem
from .models import ContactMessage, Reservation


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-transparent border-primary p-4', 'placeholder': 'Date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control bg-transparent border-primary p-4', 'placeholder': 'Time'}),
            'name': forms.TextInput(attrs={'class': 'form-control bg-transparent border-primary p-4', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-transparent border-primary p-4', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-transparent border-primary p-4', 'placeholder': 'Phone Number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Render number_of_people as a select to match the theme styling
        PEOPLE_CHOICES = [(i, str(i)) for i in range(1, 11)]
        self.fields['number_of_people'].widget = forms.Select(
            choices=PEOPLE_CHOICES,
            attrs={'class': 'custom-select bg-transparent border-primary px-4'}
        )
