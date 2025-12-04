🆘 Help People - Plataforma de Gestión de Donaciones y Ayuda Social

🌐 Sitio en producción:
https://helppeople-backend.onrender.com

---

📌 Descripción del proyecto

**Help People** es una plataforma web desarrollada con Django que permite gestionar solicitudes de ayuda, donaciones, rutas de reparto y usuarios con roles diferenciados.  
El sistema conecta donantes, beneficiarios, voluntarios y organizaciones sociales, permitiendo una distribución organizada, segura y transparente de suministros básicos.

Este proyecto combina **tecnología + impacto social real**.

---

🎯 Objetivo principal

Facilitar la ayuda social mediante un sistema que automatiza:

- Registro de donaciones
- Solicitudes de ayuda
- Distribución logística
- Control de usuarios
- Administración de recursos
- Notificaciones automáticas por correo

---

🚀 Tecnologías utilizadas

### Backend
- Python 3.13
- Django 5.2.7
- Django Rest Framework
- PostgreSQL (Render)
- Render (despliegue en la nube)
- SendGrid API (envío de correos)
- Git y GitHub

Frontend
- HTML
- CSS
- JavaScrip
- Django Templates

Base de Datos
- PostgreSQL
- Migración desde MySQL
- Admin de base de datos usando DBeaver

---

👥 Sistema de usuarios y roles

El sistema implementa control de acceso por roles:

| Rol | Permisos |
|------|-----------|
| Administrador | Acceso total al sistema |
| Recaudación | CRUD Donaciones y Contacto |
| Logística | Gestión de rutas, suministros, proveedores |
| Usuario normal | Donar y solicitar ayuda |
| Invitado | Solo puede ver el sitio |

Los usuarios sin sesión no pueden registrar donaciones ni solicitudes.

---

📮 APIs externas integradas

📧 SendGrid (Email API)
Se usa para enviar correos automáticos cuando alguien dona:

- Confirmación al donante
- Notificación interna (opcional)
- Protección con API KEY vía variables de entorno

🗺 Mapa (API externa)
Se usa una API externa de mapas para visualización de ubicación y rutas.

---

📲 REST API

Donaciones
```
GET    /api/donaciones/
POST   /api/donaciones/
GET    /api/donaciones/{id}
PUT    /api/donaciones/{id}
DELETE /api/donaciones/{id}
```

Contacto
```
GET    /api/contactos/
POST   /api/contactos/
GET    /api/contactos/{id}
PUT    /api/contactos/{id}
DELETE /api/contactos/{id}
```

---

🛠 Instalación local (opcional)

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

Configurar variables de entorno:

```
DATABASE_URL=
SENDGRID_API_KEY=
DEFAULT_FROM_EMAIL=
NOTIFICATION_EMAIL=
```

---

📂 Estructura principal

- `help_app/` → lógica principal
- `templates/` → frontend
- `static/` → estilos e imágenes
- `views.py` → vistas funcionales
- `models.py` → modelos de la BD
- `forms.py` → formularios
- `serializers.py` → REST API
- `settings.py` → configuración
- `urls.py` → rutas

---

✅ Seguridad implementada

- Protección por login
- Permisos con decoradores
- Restricción de acceso a formularios
- Protecciones en admin
- Roles separados
- Validación por servidor
- No uso de datos sensibles en código
- Uso de variables de entorno

---

📈 Estado del proyecto

✅ Sitio en producción  
✅ Donaciones funcionando  
✅ Correos funcionando  
✅ API operativa  
✅ Roles implementados  
✅ CRUD completo  
✅ Base de datos en nube  
✅ Seguridad activa  
✅ Diseño funcional  

---

MUCHAS GRACIAS
