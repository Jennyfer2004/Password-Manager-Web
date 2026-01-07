from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import PasswordEntry ,Profile
from .utils import get_cipher
from .form import CustomUserCreationForm
from .tokens import account_activation_token 
import json
from django.contrib.auth.models import User

def custom_logout(request):
    logout(request)
    return redirect('hyome')

# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UserCreationForm()
#     return render(request, 'manager/register.html', {'form': form})
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
            user.is_active = False # El usuario no puede iniciar sesión hasta que verifique
            user.save()
            
            # Crear el perfil vinculado al usuario
            Profile.objects.create(user=user)

            # Enviar correo de verificación
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
            
            return redirect('email_sent') # Una página que diga "Revisa tu correo"
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
        
        # Marcar el email como verificado en el perfil
        profile = user.profile
        profile.email_verified = True
        profile.save()
        
        login(request, user)
        return redirect('hyome') # O a donde quieras redirigirlo
    else:
        return render(request, 'manager/activation_invalid.html')
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Lógica para "Recordarme"
                if request.POST.get('remember_me'):
                    # La sesión durará 2 semanas (puedes ajustar este valor)
                    request.session.set_expiry(1209600) 
                else:
                    # La sesión expirará cuando se cierre el navegador
                    request.session.set_expiry(0)

                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'manager/login.html', {'form': form})

# Vista principal del panel (requiere estar logueado)
@login_required
def dashboard_view(request):
    entries = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'manager/dashboard.html', {'entries': entries})

# Vista para añadir una nueva contraseña
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

# Vista para obtener y descifrar una contraseña (usada por JavaScript)
@login_required
def get_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    cipher = get_cipher()
    decrypted_password = cipher.decrypt(entry.encrypted_password.encode()).decode()
    # Devolvemos la contraseña en formato JSON para que JavaScript la pueda usar
    return JsonResponse({'password': decrypted_password})

def home_view(request):
    """
    Muestra la página de bienvenida.
    Si el usuario ya está autenticado, lo redirige al panel principal.
    """
    if request.user.is_authenticated:
        # Si ya está logueado, no tiene sentido ver la página de bienvenida.
        # Lo mandamos directamente a su dashboard.
        return redirect('dashboard')
    
    # Si no está logueado, mostramos la página de bienvenida.
    return render(request, 'manager/home.html')

@login_required
def edit_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        # Obtenemos los nuevos datos del formulario
        new_website = request.POST.get('website')
        new_password = request.POST.get('password')

        # Actualizamos los campos
        entry.website = new_website
        
        # Solo volvemos a cifrar si se proporcionó una nueva contraseña
        if new_password:
            cipher = get_cipher()
            entry.encrypted_password = cipher.encrypt(new_password.encode()).decode()
        
        entry.save()
        return redirect('dashboard')
    
    # Si es GET, mostramos el formulario con los datos actuales
    return render(request, 'manager/edit_password.html', {'entry': entry})


@login_required
def delete_password_view(request, entry_id):
    entry = get_object_or_404(PasswordEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        return redirect('dashboard')
    
    # Si es GET, mostramos una página de confirmación antes de eliminar
    return render(request, 'manager/delete_password.html', {'entry': entry})
