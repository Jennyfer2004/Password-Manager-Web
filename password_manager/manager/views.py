from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse  
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry
from .utils import get_cipher
import json


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'manager/register.html', {'form': form})

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
