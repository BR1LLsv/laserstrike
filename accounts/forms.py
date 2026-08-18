from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white border-secondary'})
    )
    password_confirm = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-white border-secondary'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Ім\'я користувача (Логін)',
            'email': 'Email адреса'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Паролі не збігаються!")
        return password_confirm


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'Логін', 'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'bio']
        labels = {
            'avatar': 'Змінити аватар',
            'phone': 'Номер телефону',
            'bio': 'Позивний / Про себе'
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'phone': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': '+380...'}),
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2}),
        }