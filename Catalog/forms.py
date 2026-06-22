from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import Product

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'rounded-xl w-full px-4 py-2 border border-gray-300 focus:outline-none focus:border-dark text-sm tracking-wide bg-cream'


class LoginForm(AuthenticationForm):
    css = 'rounded-xl w-full px-4 py-2 border border-gray-300 focus:outline-none focus:border-dark text-sm tracking-wide bg-cream'
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': css,
        'placeholder': 'Enter your username',
        'autocomplete': 'username',
        'autofocus': True,
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': css,
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password',
    }))


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'is_featured']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css = 'rounded-xl w-full px-4 py-2 border border-gray-300 focus:outline-none focus:border-dark text-sm tracking-wide bg-cream'
        
        for field_name, field in self.fields.items():
            # جعل حقل الـ category (الـ select الجديد) يأخذ نفس الـ CSS
            if field_name not in ['is_featured', 'image']:
                field.widget.attrs['class'] = css
            elif field_name == 'image':
                field.widget.attrs['class'] = 'text-sm text-muted'