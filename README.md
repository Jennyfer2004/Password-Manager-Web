
# Gestor de Contraseñas Web Password Manager

Una aplicación web segura y intuitiva para gestionar todas tus contraseñas desde un solo lugar. Desarrollada con Django, esta aplicación te permite almacenar de forma segura las credenciales de tus sitios web, generar contraseñas fuertes y recuperar el acceso a tu cuenta de manera sencilla.


## Características Principales

- 🔐 **Registro y Autenticación Segura:** Crea una cuenta con una contraseña maestra segura. Inicia sesión de forma segura.
- 📧 **Verificación de Correo Electrónico:** Activación de cuenta mediante correo para garantizar la propiedad del email.
- 🛡️ **Almacenamiento Encriptado:** Tus contraseñas se guardan en la base de datos de forma encriptada.
- 🔄 **Recuperación de Contraseña:** Olvidaste tu contraseña maestra. Recupérala de forma segura a través de tu correo electrónico.
- 🎲 **Generador de Contraseñas:** Crea contraseñas seguras y personalizadas con un solo clic.
- 👁️ **Interfaz Amigable:** Diseño limpio y responsivo que facilita la gestión de tus credenciales.
- 📊 **Medidor de Fuerza de Contraseña:** Recibe retroalimentación en tiempo real sobre la seguridad de tu contraseña maestra.

## Capturas de Pantalla

<!-- Añade aquí 2-3 imágenes de tu aplicación en acción -->
<p align="center">
  <img src="./images/Captura%20desde%202026-01-08%2000-03-02.png" alt="Panel Principal" width="45%"/>
  <img src="./images/Captura%20desde%202026-01-08%2000-22-16.png" alt="Página de Login" width="45%"/>
</p>

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación y Configuración

Sigue estos pasos para poner en marcha la aplicación en tu entorno local.

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/Jennyfer2004/Password-Manager-Web.git
   cd Password-Manager-Web/password_manager
   ```

2. **Crear y Activar un Entorno Virtual**
   ```bash
   # Para Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Para macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar las Dependencias**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar la Base de Datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Configurar las Variables de Entorno**
   
   Crea un archivo llamado `.env` en la raíz del proyecto y añade la siguiente configuración. 

   ```env
   # SECRET_KEY de Django (puedes generar una nueva con: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
   SECRET_KEY='tu-secret-key-super-secreta-aqui'

   # Configuración para el envío de correos (usa una Contraseña de Aplicación de Google)
   EMAIL_HOST='smtp.gmail.com'
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER='tu_correo@gmail.com'
   EMAIL_HOST_PASSWORD='tu_contraseña_de_aplicacion_de_16_caracteres'
   DEFAULT_FROM_EMAIL='tu_correo@gmail.com'
   ```

6. **Crear un Superusuario (Opcional, para acceder al panel de administración)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el Servidor de Desarrollo**
   ```bash
   python manage.py runserver
   ```

   Abre tu navegador y ve a `http://127.0.0.1:8000/` para ver la aplicación.

## Manual de Usuario

### 1. Registro de un Nuevo Usuario

1.  En la página principal, haz clic en el enlace **"Regístrate aquí"**.
2.  Rellena el formulario con un nombre de usuario, tu correo electrónico y una contraseña maestra.
    *   **Consejo:** Usa el botón **"Generar Contraseña Segura"** para crear una contraseña fuerte.
3.  Revisa tu bandeja de entrada (y la carpeta de spam) y haz clic en el enlace de activación que te enviaremos.
4.  Una vez activada tu cuenta, ya podrás iniciar sesión.

### 2. Iniciar Sesión

1.  En la página de inicio, introduce tu nombre de usuario o correo electrónico y tu contraseña maestra.
2.  Haz clic en **"Acceder"**.

### 3. Añadir una Nueva Contraseña

1.  Una vez dentro de tu panel, busca el botón **"Añadir Nueva Contraseña"** o un formulario similar.
2.  Introduce el nombre del sitio web (ej. "GitHub"), y la contraseña, o toca la opción de generar una.
3.  Haz clic en **"Guardar"**. La contraseña se almacenará de forma encriptada.

### 4. Recuperar tu Contraseña Maestra

Si olvidas tu contraseña maestra, no te preocupes.

1.  En la página de inicio de sesión, haz clic en **"¿Olvidaste tu contraseña?"**.
2.  Introduce la dirección de correo electrónico con la que te registraste.
3.  Recibirás un correo con un enlace seguro para restablecer tu contraseña.
4.  Sigue las instrucciones del correo para crear una nueva contraseña maestra.

## Tecnologías Utilizadas

- **Backend:** Django, Python
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Base de Datos:** SQLite 
- **Librerías Clave:**
    - `zxcvbn` para el análisis de la fuerza de las contraseñas.
    - Criptografía de Django para el hashing seguro.
