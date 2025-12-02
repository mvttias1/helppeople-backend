from django.contrib import admin
from django.urls import path
from help_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.inicio, name='inicio'),
    path('sobre/', views.sobre, name='sobre'),
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/ok/', views.contacto_ok, name='contacto_ok'),
    path('dona/', views.dona, name='dona'),
    path('dona/ok/', views.dona_ok, name='dona_ok'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),


    path('panel/', views.panel, name='panel'),

    path('gestion/contactos/', views.ContactoList.as_view(), name='crud_contacto_list'),
    path('gestion/contactos/<int:pk>/', views.ContactoDetail.as_view(), name='crud_contacto_detail'),
    path('gestion/contactos/nuevo/', views.ContactoCreate.as_view(), name='crud_contacto_create'),
    path('gestion/contactos/<int:pk>/editar/', views.ContactoUpdate.as_view(), name='crud_contacto_update'),
    path('gestion/contactos/<int:pk>/eliminar/', views.ContactoDelete.as_view(), name='crud_contacto_delete'),
    path("gestion/contactos/export.csv", views.export_contactos_csv, name="export_contactos_csv"),


    path('gestion/donaciones/', views.DonacionList.as_view(), name='crud_donacion_list'),
    path('gestion/donaciones/<int:pk>/', views.DonacionDetail.as_view(), name='crud_donacion_detail'),
    path('gestion/donaciones/nueva/', views.DonacionCreate.as_view(), name='crud_donacion_create'),
    path('gestion/donaciones/<int:pk>/editar/', views.DonacionUpdate.as_view(), name='crud_donacion_update'),
    path('gestion/donaciones/<int:pk>/eliminar/', views.DonacionDelete.as_view(), name='crud_donacion_delete'),
    path("gestion/donaciones/export.csv", views.export_donaciones_csv, name="export_donaciones_csv"),


    path('gestion/usuarios/', views.UserList.as_view(), name='crud_user_list'),
    path('gestion/usuarios/nuevo/', views.UserCreate.as_view(), name='crud_user_create'),
    path('gestion/usuarios/<int:pk>/', views.UserDetail.as_view(), name='crud_user_detail'),
    path('gestion/usuarios/<int:pk>/editar/', views.UserUpdate.as_view(), name='crud_user_update'),
    path('gestion/usuarios/<int:pk>/eliminar/', views.UserDelete.as_view(), name='crud_user_delete'),



    path("gestion/proveedores/", views.ProveedorList.as_view(), name="crud_proveedor_list"),
    path("gestion/proveedores/nuevo/", views.ProveedorCreate.as_view(), name="crud_proveedor_create"),
    path("gestion/proveedores/<int:pk>/editar/", views.ProveedorUpdate.as_view(), name="crud_proveedor_update"),
    path("gestion/proveedores/<int:pk>/eliminar/", views.ProveedorDelete.as_view(), name="crud_proveedor_delete"),


    path("gestion/repartidores/", views.RepartidorList.as_view(), name="crud_repartidor_list"),
    path("gestion/repartidores/nuevo/", views.RepartidorCreate.as_view(), name="crud_repartidor_create"),
    path("gestion/repartidores/<int:pk>/editar/", views.RepartidorUpdate.as_view(), name="crud_repartidor_update"),
    path("gestion/repartidores/<int:pk>/eliminar/", views.RepartidorDelete.as_view(), name="crud_repartidor_delete"),


    path("gestion/rutas/", views.RutaList.as_view(), name="crud_ruta_list"),
    path("gestion/rutas/nuevo/", views.RutaCreate.as_view(), name="crud_ruta_create"),
    path("gestion/rutas/<int:pk>/editar/", views.RutaUpdate.as_view(), name="crud_ruta_update"),
    path("gestion/rutas/<int:pk>/eliminar/", views.RutaDelete.as_view(), name="crud_ruta_delete"),
    path("gestion/rutas/<int:pk>/beneficiarios/", views.ruta_beneficiarios, name="crud_ruta_beneficiarios"),

    path("gestion/beneficiarios/", views.BeneficiarioList.as_view(), name="crud_beneficiario_list"),
    path("gestion/beneficiarios/nuevo/", views.BeneficiarioCreate.as_view(), name="crud_beneficiario_create"),
    path("gestion/beneficiarios/<int:pk>/editar/", views.BeneficiarioUpdate.as_view(), name="crud_beneficiario_update"),
    path("gestion/beneficiarios/<int:pk>/eliminar/", views.BeneficiarioDelete.as_view(), name="crud_beneficiario_delete"),

    path("gestion/suministros/", views.SuministroList.as_view(), name="crud_suministro_list"),
    path("gestion/suministros/nuevo/", views.SuministroCreate.as_view(), name="crud_suministro_create"),
    path("gestion/suministros/<int:pk>/editar/", views.SuministroUpdate.as_view(), name="crud_suministro_update"),
    path("gestion/suministros/<int:pk>/eliminar/", views.SuministroDelete.as_view(), name="crud_suministro_delete"),

    path("gestion/proveedores/export.csv",   views.export_proveedores_csv,   name="export_proveedores_csv"),
    path("gestion/repartidores/export.csv",  views.export_repartidores_csv,  name="export_repartidores_csv"),
    path("gestion/beneficiarios/export.csv", views.export_beneficiarios_csv, name="export_beneficiarios_csv"),
    path("gestion/rutas/export.csv",         views.export_rutas_csv,         name="export_rutas_csv"),
    path("gestion/suministros/export.csv",   views.export_suministros_csv,   name="export_suministros_csv"),


]
