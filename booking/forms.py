from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'start_time', 'end_time', 'players_count', 'comment']
        widgets = {
            'booking_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control bg-dark text-white border-secondary',
                'min': date.today().isoformat()  # Не можна обирати дати у минулому
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control bg-dark text-white border-secondary'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control bg-dark text-white border-secondary'
            }),
            'players_count': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'min': 1
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'rows': 3,
                'placeholder': 'Додаткові побажання, день народження, потреба в інструкторі тощо...'
            }),
        }
        labels = {
            'booking_date': 'Дата гри',
            'start_time': 'Час початку',
            'end_time': 'Час завершення',
            'players_count': 'Кількість гравців',
            'comment': 'Коментар до замовлення (необов\'язково)',
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Номер картки",
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary fs-5 text-center',
            'placeholder': '4000 1234 5678 9010',
            'maxlength': '19',
            'id': 'cardNumber'
        })
    )
    card_holder = forms.CharField(
        label="Ім'я та Прізвище власника",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary text-uppercase',
            'placeholder': 'IVAN HAIVANIUK'
        })
    )
    expiry_date = forms.CharField(
        label="Термін дії",
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary text-center',
            'placeholder': 'MM/YY',
            'maxlength': '5'
        })
    )
    cvv = forms.CharField(
        label="CVV / CVC",
        max_length=3,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary text-center',
            'placeholder': '***',
            'maxlength': '3'
        })
    )