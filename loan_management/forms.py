from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Application, CustomUser  # Ensure this imports your custom user model
from django.core.exceptions import ValidationError  # Import ValidationError for custom validation

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add an email field if it's part of your user model

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # Include other fields if necessary

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username cannot be empty.")
        # Temporarily skip uniqueness validation for username
        # if CustomUser.objects.filter(username=username).exists():
        #     raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email cannot be empty.")
        
        # Temporarily skip email uniqueness validation
        # if CustomUser.objects.filter(email=email).exists():
        #     raise ValidationError("A user with this email already exists.")
        
        return email

# Custom Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

# Loan Application Form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['employer_name', 'job_title', 'monthly_income', 'amount', 'purpose', 'duration']  # Remove 'duration' if it's not part of your model

    # Additional validations
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError("Loan amount must be greater than zero.")
        return amount

    def clean_purpose(self):
        purpose = self.cleaned_data.get('purpose')
        if not purpose:
            raise ValidationError("Purpose field cannot be empty.")
        return purpose
