from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models.user import User

class ClientLoginForm(forms.Form):
    """
    Form for client login.
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
    )

class ClientRegistrationForm(UserCreationForm):
    """
    Form for client registration.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'user_address')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CLIENT'
        if commit:
            user.save()
        return user
