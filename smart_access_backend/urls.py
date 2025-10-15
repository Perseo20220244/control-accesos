"""
URL configuration for smart_access_backend project.
Sistema de Control de Accesos Inteligente para Entornos Educativos
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Personalización del panel de administración
admin.site.site_header = "Sistema de Control de Accesos Inteligente"
admin.site.site_title = "Control de Accesos"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
