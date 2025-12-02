# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Beneficiario(models.Model):
    id_beneficiario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beneficiario'


class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    region = models.CharField(max_length=60)
    comuna = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    tipo_comunidad = models.CharField(max_length=18)
    nombre_comunidad = models.CharField(max_length=120, blank=True, null=True)
    descripcion_necesidad = models.TextField()
    cantidad_personas = models.IntegerField(blank=True, null=True)
    prioridad = models.CharField(max_length=5, blank=True, null=True)
    acepta_contacto = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacto'


class Coordinador(models.Model):
    id_coordinador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    contrasena = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'coordinador'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Donacion(models.Model):
    id_donacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    documento = models.CharField(max_length=30)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    certificado = models.CharField(max_length=2)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donacion'


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Repartidor(models.Model):
    id_repartidor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    vehiculo = models.CharField(max_length=100, blank=True, null=True)
    id_coordinador = models.ForeignKey(Coordinador, models.DO_NOTHING, db_column='id_coordinador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repartidor'


class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    id_repartidor = models.ForeignKey(Repartidor, models.DO_NOTHING, db_column='id_repartidor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ruta'


class RutaBeneficiario(models.Model):
    pk = models.CompositePrimaryKey('id_ruta', 'id_beneficiario')
    id_ruta = models.ForeignKey(Ruta, models.DO_NOTHING, db_column='id_ruta')
    id_beneficiario = models.ForeignKey(Beneficiario, models.DO_NOTHING, db_column='id_beneficiario')

    class Meta:
        managed = False
        db_table = 'ruta_beneficiario'


class SolicitudAyuda(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    nombre_solicitante = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    region = models.CharField(max_length=60)
    comuna = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    tipo_comunidad = models.CharField(max_length=18)
    nombre_comunidad = models.CharField(max_length=120, blank=True, null=True)
    descripcion_necesidad = models.TextField()
    cantidad_personas = models.IntegerField(blank=True, null=True)
    prioridad = models.CharField(max_length=5, blank=True, null=True)
    acepta_contacto = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitud_ayuda'


class Suministro(models.Model):
    id_suministro = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedor, models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    id_ruta = models.ForeignKey(Ruta, models.DO_NOTHING, db_column='id_ruta', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'suministro'
