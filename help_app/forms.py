from django import forms
from django.core.exceptions import ValidationError
from .models import Contacto, Donacion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Proveedor, Repartidor, Ruta, Beneficiario, Suministro

def clean_correo(self):
    correo = self.cleaned_data.get("correo", "")
    try:
        validate_email(correo)
    except ValidationError:
        raise ValidationError("Correo inválido.")
    return correo

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


DIGITS = set("0123456789")
def only_digits(s: str) -> str:
    return "".join(ch for ch in str(s) if ch in DIGITS)

TIPO_COMUNIDAD_CHOICES = [
    ("Junta de Vecinos", "Junta de Vecinos"),
    ("Comunidad Indígena", "Comunidad Indígena"),
    ("Campamento", "Campamento"),
    ("Fundación", "Fundación"),
    ("Colegio", "Colegio"),
    ("Otra", "Otra"),
]
PRIORIDAD_CHOICES = [
    ("alta", "Alta"),
    ("media", "Media"),
    ("baja", "Baja"),
]

class ContactoForm(forms.ModelForm):
    telefono = forms.CharField(required=True, max_length=20)
    cantidad_personas = forms.CharField(required=False)

    tipo_comunidad = forms.ChoiceField(choices=TIPO_COMUNIDAD_CHOICES, required=True)
    prioridad = forms.ChoiceField(choices=PRIORIDAD_CHOICES, required=True)
    acepta_contacto = forms.BooleanField(required=False)

    class Meta:
        model = Contacto
        fields = [
            "nombre", "correo", "telefono",
            "region", "comuna", "direccion",
            "tipo_comunidad", "nombre_comunidad",
            "descripcion_necesidad",
            "cantidad_personas",
            "prioridad", "acepta_contacto",
        ]
        widgets = {"descripcion_necesidad": forms.Textarea(attrs={"rows": 4})}

    def clean_telefono(self):
        num = only_digits(self.cleaned_data.get("telefono", ""))
        if not num:
            raise ValidationError("Ingresa tu teléfono.")
        return num

    def clean_cantidad_personas(self):
        raw = self.cleaned_data.get("cantidad_personas", "")
        if raw in ("", None, " "):
            return None
        digits = only_digits(raw)
        if not digits:
            raise ValidationError("Ingresa un número entero positivo.")
        value = int(digits)
        if value < 1:
            raise ValidationError("Debe ser 1 o más.")
        return value

class DonacionForm(forms.ModelForm):
    telefono = forms.CharField(required=True, max_length=20)
    certificado = forms.ChoiceField(
        required=True,
        choices=(("SI", "Sí"), ("NO", "No")),
        widget=forms.RadioSelect,
        initial="NO",
        error_messages={"required": "Selecciona Sí o No."},
    )

    class Meta:
        model = Donacion
        fields = ["nombre", "apellido", "rut", "documento", "correo", "telefono", "certificado"]

    def clean_telefono(self):
        num = only_digits(self.cleaned_data.get("telefono", ""))
        if not num:
            raise ValidationError("Ingresa tu teléfono.")
        return num

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "email", "stock"]

class RepartidorForm(forms.ModelForm):
    class Meta:
        model = Repartidor
        fields = ["nombre", "email", "vehiculo", "id_coordinador"]

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ["descripcion", "id_repartidor"]

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ["nombre", "ubicacion"]

class SuministroForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ["id_proveedor", "id_ruta", "cantidad", "fecha"]
        widgets = {"fecha": forms.DateInput(attrs={"type": "date"})}
