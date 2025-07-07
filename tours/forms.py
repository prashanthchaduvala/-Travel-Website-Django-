from django import forms
from .models import CustomUser,Tour
from django.contrib.auth.forms import UserCreationForm
# forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password1', 'password2']


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        exclude = ['user', 'created_at']


class ToursForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'country', 'city', 'duration_days', 'price', 'availability_date', 'image', 'is_active']
        widgets = {
            'availability_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TourForms(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'country', 'city', 'duration_days', 'price', 'availability_date', 'image', 'is_active']
        widgets = {
            'availability_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password")
        if not user.is_active:
            raise forms.ValidationError("Account not active. Check your email to verify.")
        cleaned_data['user'] = user
        return cleaned_data
