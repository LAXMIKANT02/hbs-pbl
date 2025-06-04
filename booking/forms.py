from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HotelRating, Hotel

class HotelRatingForm(forms.ModelForm):
    class Meta:
        model = HotelRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'type': 'number'})
        }
        labels = {
            'rating': 'Rate this hotel (1-5)'
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class HotelForm(forms.ModelForm):
    room_type = forms.CharField(max_length=100, required=True, label='Room Type')
    price = forms.DecimalField(max_digits=8, decimal_places=2, required=True, label='Price per Night')

    class Meta:
        model = Hotel
        fields = ['name', 'location', 'description', 'image']
