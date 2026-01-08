from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm, SetPasswordForm
from django.http import JsonResponse  
from django.contrib.auth import logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import PasswordEntry ,Profile
from .utils import get_cipher
from .form import CustomUserCreationForm, CustomAuthenticationForm 
from .tokens import account_activation_token 
import json
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

def custom_logout(request):
    logout(request)
    return redirect('hyome')

def email_sent_view(request):
    """
    Muestra una página confirmando que el correo de verificación ha sido enviado.
    """
    return render(request, 'manager/email_sent.html')
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()
            
            Profile.objects.create(user=user)

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta en Password Manager'
            message = render_to_string('manager/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            return redirect('email_sent') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'manager/register.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        profile = user.profile
        profile.email_verified = True
        profile.save()
        
        login(request, user)
        return redirect('hyome') 
    else:
        return render(request, 'manager/activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session.set_expiry(0)

                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'manager/login.html', {'form': form})

@login_required
def dashboard_view(request):
    entries = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'manager/dashboard.html', {'entries': entries})

@login_required
def add_password_view(request):
    if request.method == 'POST':
        website = request.POST.get('website')
        password = request.POST.get('password')
        
        cipher = get_cipher()
        encrypted_password = cipher.encrypt(password.encode()).decode()
        
        PasswordEntry.objects.create(
            user=request.user,
            website=website,
            encrypted_password=encrypted_password
        )
        return redirect('dashboard')
    return render(request, 'manager/add_password.html')

@login_required
def get_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    cipher = get_cipher()
    decrypted_password = cipher.decrypt(entry.encrypted_password.encode()).decode()

    return JsonResponse({'password': decrypted_password})

def home_view(request):
    """
    Muestra la página de bienvenida.
    Si el usuario ya está autenticado, lo redirige al panel principal.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'manager/home.html')

@login_required
def edit_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        new_website = request.POST.get('website')
        new_password = request.POST.get('password')

        entry.website = new_website
        
        if new_password:
            cipher = get_cipher()
            entry.encrypted_password = cipher.encrypt(new_password.encode()).decode()
        
        entry.save()
        return redirect('dashboard')
    
    return render(request, 'manager/edit_password.html', {'entry': entry})


@login_required
def delete_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        return redirect('dashboard')
    
    return render(request, 'manager/delete_password.html', {'entry': entry})


def password_reset_request_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Recuperación de Contraseña - Password Manager"
                    
                    context = {
                        'user': user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http', 
                    }
                    
                    email_body = render_to_string('manager/password_reset_email.html', context)
                    
                    email = EmailMessage(subject, email_body, to=[user.email])
                    email.send()
            

            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'manager/password_reset.html', {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'manager/password_reset_confirm.html'
    form_class = SetPasswordForm

    success_url = '/login/password-reset-complete/'

def password_reset_done_view(request):
    return render(request, 'manager/password_reset_done.html')

def password_reset_complete_view(request):
    return render(request, 'manager/password_reset_complete.html')