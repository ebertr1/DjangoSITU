from django.contrib import admin
from django.urls import path
from appSITUweb import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin/', admin.site.urls),
    path('pasajeros/', views.pasajeros, name='pasajeros'),
    path('pasajerosEdit/<int:id>/', views.pasajerosEdit, name='pasajerosEdit'),

    # 🔥 nueva vista que te di antes
    path('pago/', views.simular_pago, name='simular_pago'),
    path('tarjeta/', views.tarjeta, name='tarjeta'),
    path('tarjeta/recargar/<int:id>/', views.recargar_saldo, name='recargar_saldo'),
]