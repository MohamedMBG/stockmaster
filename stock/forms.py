from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Product, Category, Supplier, StockTransaction, Order

User = get_user_model()

class LoginForm(AuthenticationForm):
    """Custom login form with styled fields."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
    }))

class ClientRegistrationForm(UserCreationForm):
    """Registration form for clients only."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name',
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name',
    }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your phone number',
    }))
    user_address = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your address (optional)',
        'rows': 3,
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_address', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set role to CLIENT by default
        self.instance.role = User.Role.CLIENT
        
        # Style form fields
        for field_name in self.fields:
            if 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': f'Enter your {field_name.replace("_", " ")}',
                })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.user_address = self.cleaned_data.get('user_address', '')
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user

class SupervisorCreationForm(UserCreationForm):
    """Form for admins to create supervisor accounts."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set role to SUPERVISOR by default
        self.instance.role = User.Role.SUPERVISOR
        
        # Style form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
            })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = User.Role.SUPERVISOR
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'user_address')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'user_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProfileImageForm(forms.ModelForm):
    """Form for updating profile image."""
    class Meta:
        model = User
        fields = ('profile_image',)
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    """Form for adding/editing products."""
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'supplier', 'unit_price', 
                  'quantity', 'reorder_level', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    """Form for adding/editing categories."""
    class Meta:
        model = Category
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SupplierForm(forms.ModelForm):
    """Form for adding/editing suppliers."""
    class Meta:
        model = Supplier
        fields = ('name', 'contact_person', 'email', 'phone', 'address')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StockTransactionForm(forms.ModelForm):
    """Form for recording stock transactions."""
    class Meta:
        model = StockTransaction
        fields = ('product', 'transaction_type', 'quantity', 'notes')
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OrderForm(forms.ModelForm):
    """Form for creating/editing orders."""
    class Meta:
        model = Order
        fields = ('client', 'status')
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
