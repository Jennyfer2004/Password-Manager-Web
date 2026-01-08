from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Un formulario de registro que impide correos duplicados.
    """
    email = forms.EmailField(
        required=True, 
        help_text='Requerido. Introduce una dirección de correo electrónico válida.'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):

        email = self.cleaned_data.get('email').lower()  
        if User.objects.filter(email__iexact=email).exists():

            raise ValidationError(
                'Este correo electrónico ya está registrado. Por favor, utiliza otro correo.',
                code='email_exists'
            )
        
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    """
    Un formulario de autenticación que permite iniciar sesión con nombre de usuario o correo electrónico.
    """
    username = forms.CharField(
        label="Usuario o Correo Electrónico",
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                pass
        return username