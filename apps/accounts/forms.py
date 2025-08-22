# apps/accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class DentistAuthForm(AuthenticationForm):
    """
    Login: permite ingresar 'correo o usuario'.
    Como en el registro seteamos username = email, el usuario
    puede iniciar sesión escribiendo su correo.
    """
    username = forms.CharField(
        label="Correo o usuario",
        widget=forms.TextInput(attrs={
            "autocomplete": "username",
            "placeholder": "tu@correo.com",
            "class": "form-control",
        })
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "••••••••",
            "class": "form-control",
        })
    )


class DentistSignupForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre",
            "class": "form-control",
        })
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Apellidos",
            "class": "form-control",
        })
    )
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={
            "placeholder": "tu@correo.com",
            "class": "form-control",
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # No pedimos username al usuario (lo generamos desde el email)
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower().strip()
        user.email = email
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()

        # Si el modelo tiene username, lo seteamos al email
        if hasattr(user, "username") and not getattr(user, "username", ""):
            user.username = email

        if commit:
            user.save()
        return user
