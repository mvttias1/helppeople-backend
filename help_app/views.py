from datetime import timedelta
import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db import connection
from django.db.models import Count, Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RegistroForm, ContactoForm, DonacionForm
from .models import (
    Contacto, Donacion,
    Proveedor, Repartidor, Beneficiario,
    Ruta, Suministro,
)



def in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()

def es_admin(user):
    return user.is_staff or user.is_superuser

def es_recaudacion(user):
    return es_admin(user) or in_group(user, "Recaudación")

def es_logistica(user):
    return es_admin(user) or in_group(user, "Logística")

def es_privilegiado(user):

    return es_admin(user) or in_group(user, "Recaudación") or in_group(user, "Logística")


only_admin = [login_required, user_passes_test(es_admin)]


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirección por rol
            if es_privilegiado(user):
                return redirect("panel")
            return redirect("inicio")
        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("inicio")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("inicio")


def register_view(request):
    """Registro de usuarios normales (no staff)."""
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, "Cuenta creada. Ahora puedes iniciar sesión.")
            return redirect("inicio")
    else:
        form = RegistroForm()
    return render(request, "register.html", {"form": form})


def inicio(request):
    return render(request, "inicio.html")

def sobre(request):
    return render(request, "sobre.html")

def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contacto_ok")
    else:
        form = ContactoForm()
    return render(request, "contacto.html", {"form": form})

def contacto_ok(request):
    return render(request, "ok.html", {"mensaje": "¡Recibimos tu solicitud de ayuda! Nos contactaremos pronto."})

def dona(request):
    if request.method == "POST":
        form = DonacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dona_ok")
    else:
        form = DonacionForm()
    return render(request, "dona.html", {"form": form})

def dona_ok(request):
    return render(request, "ok.html", {"mensaje": "¡Gracias por tu donación!"})


@login_required
@user_passes_test(es_privilegiado)  
def panel(request):
    is_admin = es_admin(request.user)
    is_rec   = es_recaudacion(request.user)
    is_log   = es_logistica(request.user)

    ctx = {
        "is_admin": is_admin,
        "is_rec":   is_rec,
        "is_log":   is_log,
    }

    if is_admin or is_rec:
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        ctx.update({
            "total_contactos": Contacto.objects.count(),
            "nuevos_contactos_7d": Contacto.objects.filter(fecha__isnull=False, fecha__gte=seven_days_ago).count(),
            "total_donaciones": Donacion.objects.count(),
            "nuevas_donaciones_7d": Donacion.objects.filter(fecha__isnull=False, fecha__gte=seven_days_ago).count(),
        })

    if is_admin or is_log:
        ctx.update({
            "total_proveedores":  Proveedor.objects.count(),
            "total_repartidores": Repartidor.objects.count(),
            "total_beneficiarios": Beneficiario.objects.count(),
            "total_rutas":        Ruta.objects.count(),
            "total_suministros":  Suministro.objects.count(),
        })


    if is_admin:
        ctx.update({
            "total_usuarios": User.objects.count(),
        })

    return render(request, "panel.html", ctx)




@login_required
@user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))
def export_contactos_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="contactos.csv"'
    w = csv.writer(resp)
    w.writerow(["ID","Nombre","Correo","Teléfono","Región","Comuna","Prioridad","Acepta contacto","Fecha"])
    for c in Contacto.objects.order_by("id_contacto"):
        acepta = ""
        if c.acepta_contacto is not None:
            try:
                acepta = "SI" if int(c.acepta_contacto) == 1 else "NO"
            except Exception:
                acepta = "NO"
        fecha_txt = c.fecha.strftime("%Y-%m-%d %H:%M") if c.fecha else ""
        w.writerow([c.id_contacto, c.nombre, c.correo, c.telefono, c.region, c.comuna, c.prioridad or "", acepta, fecha_txt])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))
def export_donaciones_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="donaciones.csv"'
    w = csv.writer(resp)
    w.writerow(["ID","Nombre","Apellido","RUT","Documento","Correo","Teléfono","Certificado","Fecha"])
    for d in Donacion.objects.order_by("id_donacion"):
        fecha_txt = d.fecha.strftime("%Y-%m-%d %H:%M") if d.fecha else ""
        w.writerow([d.id_donacion, d.nombre, d.apellido, d.rut, d.documento, d.correo, d.telefono, d.certificado, fecha_txt])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def export_proveedores_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="proveedores.csv"'
    w = csv.writer(resp)
    w.writerow(["id_proveedor","nombre","email","stock"])
    for x in Proveedor.objects.order_by("id_proveedor"):
        w.writerow([x.id_proveedor, x.nombre, x.email or "", x.stock or 0])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def export_repartidores_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="repartidores.csv"'
    w = csv.writer(resp)
    w.writerow(["id_repartidor","nombre","email","vehiculo","coordinador_id"])
    for x in Repartidor.objects.order_by("id_repartidor"):
        w.writerow([x.id_repartidor, x.nombre, x.email or "", x.vehiculo or "", getattr(x.id_coordinador, "id_coordinador", "")])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def export_beneficiarios_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="beneficiarios.csv"'
    w = csv.writer(resp)
    w.writerow(["id_beneficiario","nombre","ubicacion"])
    for x in Beneficiario.objects.order_by("id_beneficiario"):
        w.writerow([x.id_beneficiario, x.nombre, x.ubicacion or ""])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def export_rutas_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="rutas.csv"'
    w = csv.writer(resp)
    w.writerow(["id_ruta","descripcion","repartidor_id","repartidor_nombre"])
    for x in Ruta.objects.order_by("id_ruta"):
        w.writerow([x.id_ruta, x.descripcion or "", getattr(x.id_repartidor, "id_repartidor", ""), getattr(x.id_repartidor, "nombre", "")])
    return resp

@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def export_suministros_csv(request):
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="suministros.csv"'
    w = csv.writer(resp)
    w.writerow(["id_suministro","proveedor","ruta","cantidad","fecha"])
    for x in Suministro.objects.order_by("id_suministro"):
        fecha_txt = x.fecha.strftime("%Y-%m-%d") if x.fecha else ""
        w.writerow([x.id_suministro, getattr(x.id_proveedor, "nombre", ""), getattr(x.id_ruta, "id_ruta", ""), x.cantidad or 0, fecha_txt])
    return resp


@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class ContactoList(ListView):
    model = Contacto
    template_name = "crud/contacto_list.html"
    paginate_by = 15
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset().order_by('-fecha')
        q = self.request.GET.get("q", "").strip()
        region = self.request.GET.get("region", "").strip()
        prioridad = self.request.GET.get("prioridad", "").strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(correo__icontains=q) |
                Q(telefono__icontains=q) |
                Q(descripcion_necesidad__icontains=q)
            )
        if region:
            qs = qs.filter(region__icontains=region)
        if prioridad:
            qs = qs.filter(prioridad=prioridad)
        return qs

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class ContactoDetail(DetailView):
    model = Contacto
    template_name = "crud/contacto_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class ContactoCreate(CreateView):
    model = Contacto
    form_class = ContactoForm
    template_name = "crud/contacto_form.html"
    success_url = reverse_lazy("crud_contacto_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class ContactoUpdate(UpdateView):
    model = Contacto
    form_class = ContactoForm
    template_name = "crud/contacto_form.html"
    success_url = reverse_lazy("crud_contacto_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class ContactoDelete(DeleteView):
    model = Contacto
    template_name = "crud/contacto_confirm_delete.html"
    success_url = reverse_lazy("crud_contacto_list")


@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class DonacionList(ListView):
    model = Donacion
    template_name = "crud/donacion_list.html"
    paginate_by = 20
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset().order_by('-fecha')
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q) |
                Q(rut__icontains=q) |
                Q(correo__icontains=q) |
                Q(documento__icontains=q)
            )
        return qs

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class DonacionDetail(DetailView):
    model = Donacion
    template_name = "crud/donacion_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class DonacionCreate(CreateView):
    model = Donacion
    form_class = DonacionForm
    template_name = "crud/donacion_form.html"
    success_url = reverse_lazy("crud_donacion_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class DonacionUpdate(UpdateView):
    model = Donacion
    form_class = DonacionForm
    template_name = "crud/donacion_form.html"
    success_url = reverse_lazy("crud_donacion_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_recaudacion(u))], name="dispatch")
class DonacionDelete(DeleteView):
    model = Donacion
    template_name = "crud/donacion_confirm_delete.html"
    success_url = reverse_lazy("crud_donacion_list")


@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class ProveedorList(ListView):
    model = Proveedor
    template_name = "crud/proveedor_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("nombre")
        q = self.request.GET.get("q", "").strip()
        stock_min = self.request.GET.get("stock_min", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q))
        if stock_min.isdigit():
            qs = qs.filter(stock__gte=int(stock_min))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["stock_min"] = self.request.GET.get("stock_min", "")
        return ctx

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class ProveedorDetail(DetailView):
    model = Proveedor
    template_name = "crud/proveedor_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class ProveedorCreate(CreateView):
    model = Proveedor
    fields = "__all__"
    template_name = "crud/proveedor_form.html"
    success_url = reverse_lazy("crud_proveedor_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class ProveedorUpdate(UpdateView):
    model = Proveedor
    fields = "__all__"
    template_name = "crud/proveedor_form.html"
    success_url = reverse_lazy("crud_proveedor_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class ProveedorDelete(DeleteView):
    model = Proveedor
    template_name = "crud/proveedor_confirm_delete.html"
    success_url = reverse_lazy("crud_proveedor_list")



@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RepartidorList(ListView):
    model = Repartidor
    template_name = "crud/repartidor_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("nombre")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(email__icontains=q) | Q(vehiculo__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RepartidorDetail(DetailView):
    model = Repartidor
    template_name = "crud/repartidor_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RepartidorCreate(CreateView):
    model = Repartidor
    fields = "__all__"
    template_name = "crud/repartidor_form.html"
    success_url = reverse_lazy("crud_repartidor_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RepartidorUpdate(UpdateView):
    model = Repartidor
    fields = "__all__"
    template_name = "crud/repartidor_form.html"
    success_url = reverse_lazy("crud_repartidor_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RepartidorDelete(DeleteView):
    model = Repartidor
    template_name = "crud/repartidor_confirm_delete.html"
    success_url = reverse_lazy("crud_repartidor_list")



@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class BeneficiarioList(ListView):
    model = Beneficiario
    template_name = "crud/beneficiario_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("nombre")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(ubicacion__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class BeneficiarioDetail(DetailView):
    model = Beneficiario
    template_name = "crud/beneficiario_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class BeneficiarioCreate(CreateView):
    model = Beneficiario
    fields = "__all__"
    template_name = "crud/beneficiario_form.html"
    success_url = reverse_lazy("crud_beneficiario_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class BeneficiarioUpdate(UpdateView):
    model = Beneficiario
    fields = "__all__"
    template_name = "crud/beneficiario_form.html"
    success_url = reverse_lazy("crud_beneficiario_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class BeneficiarioDelete(DeleteView):
    model = Beneficiario
    template_name = "crud/beneficiario_confirm_delete.html"
    success_url = reverse_lazy("crud_beneficiario_list")

# ==========================================
# CRUD Ruta (Logística o Admin)
# ==========================================

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RutaList(ListView):
    model = Ruta
    template_name = "crud/ruta_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("-id_ruta")
        rep = self.request.GET.get("rep", "").strip()
        if rep:
            qs = qs.filter(id_repartidor__nombre__icontains=rep)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["rep"] = self.request.GET.get("rep", "")
        return ctx

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RutaDetail(DetailView):
    model = Ruta
    template_name = "crud/ruta_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RutaCreate(CreateView):
    model = Ruta
    fields = "__all__"
    template_name = "crud/ruta_form.html"
    success_url = reverse_lazy("crud_ruta_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RutaUpdate(UpdateView):
    model = Ruta
    fields = "__all__"
    template_name = "crud/ruta_form.html"
    success_url = reverse_lazy("crud_ruta_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class RutaDelete(DeleteView):
    model = Ruta
    template_name = "crud/ruta_confirm_delete.html"
    success_url = reverse_lazy("crud_ruta_list")



@login_required
@user_passes_test(lambda u: es_admin(u) or es_logistica(u))
def ruta_beneficiarios(request, pk):
    """Listar y asignar beneficiarios a una ruta usando SQL directo sobre ruta_beneficiario."""
    ruta = get_object_or_404(Ruta, pk=pk)
    todos = Beneficiario.objects.order_by("nombre")

    # IDs ya asignados
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_beneficiario FROM ruta_beneficiario WHERE id_ruta = %s", [pk])
        asignados_ids = {row[0] for row in cursor.fetchall()}

    if request.method == "POST":
        nuevos_ids = {int(x) for x in request.POST.getlist("beneficiarios")}

        # Reemplazar asignaciones
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM ruta_beneficiario WHERE id_ruta = %s", [pk])
            for b_id in nuevos_ids:
                cursor.execute(
                    "INSERT INTO ruta_beneficiario (id_ruta, id_beneficiario) VALUES (%s, %s)",
                    [pk, b_id]
                )

        messages.success(request, "Beneficiarios actualizados.")
        return redirect("crud_ruta_beneficiarios", pk=pk)

    return render(request, "crud/ruta_beneficiarios.html", {
        "ruta": ruta,
        "todos": todos,
        "asignados_ids": asignados_ids,
    })


@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class SuministroList(ListView):
    model = Suministro
    template_name = "crud/suministro_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("-id_suministro")
        prov = self.request.GET.get("prov", "").strip()
        if prov:
            qs = qs.filter(id_proveedor__nombre__icontains=prov)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["prov"] = self.request.GET.get("prov", "")
        return ctx

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class SuministroDetail(DetailView):
    model = Suministro
    template_name = "crud/suministro_detail.html"
    context_object_name = "obj"
    pk_url_kwarg = "pk"

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class SuministroCreate(CreateView):
    model = Suministro
    fields = "__all__"
    template_name = "crud/suministro_form.html"
    success_url = reverse_lazy("crud_suministro_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class SuministroUpdate(UpdateView):
    model = Suministro
    fields = "__all__"
    template_name = "crud/suministro_form.html"
    success_url = reverse_lazy("crud_suministro_list")

@method_decorator([login_required, user_passes_test(lambda u: es_admin(u) or es_logistica(u))], name="dispatch")
class SuministroDelete(DeleteView):
    model = Suministro
    template_name = "crud/suministro_confirm_delete.html"
    success_url = reverse_lazy("crud_suministro_list")


@method_decorator(only_admin, name="dispatch")
class UserList(ListView):
    model = User
    template_name = "crud/user_list.html"
    paginate_by = 20
    context_object_name = "items"
    def get_queryset(self):
        qs = super().get_queryset().order_by("-date_joined")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx

@method_decorator(only_admin, name="dispatch")
class UserDetail(DetailView):
    model = User
    template_name = "crud/user_detail.html"
    context_object_name = "obj"

@method_decorator(only_admin, name="dispatch")
class UserCreate(CreateView):
    model = User
    fields = ["username", "email", "is_staff", "is_superuser", "is_active", "password"]
    template_name = "crud/user_form.html"
    success_url = reverse_lazy("crud_user_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        raw = form.cleaned_data.get("password", "")
        if raw:
            obj.set_password(raw)
        else:
            obj.set_password("Cambiar123!")
        obj.save()
        return redirect(self.success_url)

@method_decorator(only_admin, name="dispatch")
class UserUpdate(UpdateView):
    model = User
    fields = ["username", "email", "is_staff", "is_superuser", "is_active"]
    template_name = "crud/user_form.html"
    success_url = reverse_lazy("crud_user_list")

@method_decorator(only_admin, name="dispatch")
class UserDelete(DeleteView):
    model = User
    template_name = "crud/user_confirm_delete.html"
    success_url = reverse_lazy("crud_user_list")
