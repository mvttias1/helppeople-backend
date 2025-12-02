from django.contrib import admin

try:
    from .models import Contacto, Donacion
except Exception:
    Contacto = None
    Donacion = None

def display_for(model, preferred):
    if not model:
        return []
    model_fields = [f.name for f in model._meta.fields]
    picked = [name for name in preferred if name in model_fields]
    return picked or model_fields[:3]

def filters_for(model, preferred):
    if not model:
        return []
    model_fields = [f.name for f in model._meta.fields]
    return [name for name in preferred if name in model_fields]

if Contacto:
    class ContactoAdmin(admin.ModelAdmin):
        list_display = display_for(
            Contacto,
            ["nombre", "correo", "telefono", "region", "comuna", "prioridad", "creado_en"]
        )
        list_filter = filters_for(
            Contacto,
            ["prioridad", "tipo_comunidad", "region", "comuna", "creado_en"]
        )
        search_fields = [f.name for f in Contacto._meta.fields if f.get_internal_type() in ("CharField","TextField","EmailField")]

    admin.site.register(Contacto, ContactoAdmin)

if Donacion:
    class DonacionAdmin(admin.ModelAdmin):
        list_display = display_for(
            Donacion,
            ["nombre", "apellido", "rut", "correo", "certificado", "creado_en"]
        )
        list_filter = filters_for(
            Donacion,
            ["certificado", "creado_en"]
        )
        search_fields = [f.name for f in Donacion._meta.fields if f.get_internal_type() in ("CharField","TextField","EmailField")]

    admin.site.register(Donacion, DonacionAdmin)
