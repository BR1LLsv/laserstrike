from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'start_time', 'end_time', 'players_count']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'players_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16, 
        min_length=16, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000 0000 0000 0000'})
    )
    card_expiry = forms.CharField(
        max_length=5, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    card_cvv = forms.CharField(
        max_length=3, 
        min_length=3, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '123'})
    )