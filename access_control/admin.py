from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Door, LockState


# Inline para UserProfile en User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Control de Accesos'
    fk_name = 'user'
    fields = ('rol', 'codigo_acceso', 'telefono', 'activo')
    
    def get_readonly_fields(self, request, obj=None):
        """
        El código de acceso es editable solo para:
        - Superusuarios
        - Staff con permisos de cambio de UserProfile
        """
        if request.user.is_superuser:
            return []
        if request.user.has_perm('access_control.change_userprofile'):
            return []
        # Para usuarios sin permisos, el código es solo lectura
        return ['codigo_acceso']


# Extender User Admin para incluir UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'profile__rol')
    
    # Habilitar cambio de contraseña en el admin
    change_password_form = None  # Usa el formulario por defecto de Django
    
    def get_rol(self, obj):
        """Mostrar el rol del perfil si existe"""
        try:
            return obj.profile.get_rol_display()
        except UserProfile.DoesNotExist:
            return '-'
    get_rol.short_description = 'Rol'
    get_rol.admin_order_field = 'profile__rol'


# Desregistrar el User admin original y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Administración de perfiles de usuario con roles y códigos de acceso.
    """
    list_display = [
        'get_nombre_completo', 'rol', 'codigo_acceso', 'telefono', 
        'activo', 'fecha_creacion'
    ]
    list_filter = ['rol', 'activo', 'fecha_creacion']
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'codigo_acceso', 'telefono'
    ]
    ordering = ['user__username']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    list_per_page = 25
    
    def get_nombre_completo(self, obj):
        """Mostrar nombre completo o username"""
        return obj.user.get_full_name() or obj.user.username
    get_nombre_completo.short_description = 'Usuario'
    get_nombre_completo.admin_order_field = 'user__username'
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Control de Acceso', {
            'fields': ('rol', 'codigo_acceso', 'activo')
        }),
        ('Información de Contacto', {
            'fields': ('telefono',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """
        El código de acceso es editable para:
        - Superusuarios
        - Staff con permisos de cambio de UserProfile
        """
        readonly = list(self.readonly_fields)
        
        # Si no es superusuario y no tiene permisos, código de acceso es readonly
        if not request.user.is_superuser and not request.user.has_perm('access_control.change_userprofile'):
            readonly.append('codigo_acceso')
        
        return readonly


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    """
    Administración de puertas del sistema.
    """
    list_display = [
        'nombre', 'ubicacion', 'estado', 'activa', 
        'fecha_creacion'
    ]
    list_filter = ['estado', 'activa', 'fecha_creacion']
    search_fields = ['nombre', 'ubicacion', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'ubicacion', 'descripcion')
        }),
        ('Estado', {
            'fields': ('estado', 'activa')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marcar_como_abierta', 'marcar_como_cerrada', 'activar_puertas', 'desactivar_puertas']
    
    def marcar_como_abierta(self, request, queryset):
        """Acción para abrir puertas seleccionadas"""
        updated = queryset.update(estado='ABIERTA')
        self.message_user(request, f'{updated} puerta(s) marcada(s) como ABIERTA.')
    marcar_como_abierta.short_description = "Marcar como ABIERTA"
    
    def marcar_como_cerrada(self, request, queryset):
        """Acción para cerrar puertas seleccionadas"""
        updated = queryset.update(estado='CERRADA')
        self.message_user(request, f'{updated} puerta(s) marcada(s) como CERRADA.')
    marcar_como_cerrada.short_description = "Marcar como CERRADA"
    
    def activar_puertas(self, request, queryset):
        """Acción para activar puertas"""
        updated = queryset.update(activa=True)
        self.message_user(request, f'{updated} puerta(s) activada(s).')
    activar_puertas.short_description = "Activar puertas seleccionadas"
    
    def desactivar_puertas(self, request, queryset):
        """Acción para desactivar puertas"""
        updated = queryset.update(activa=False)
        self.message_user(request, f'{updated} puerta(s) desactivada(s).')
    desactivar_puertas.short_description = "Desactivar puertas seleccionadas"


@admin.register(LockState)
class LockStateAdmin(admin.ModelAdmin):
    """
    Administración del estado de seguros de puertas.
    """
    list_display = [
        'puerta', 'activo', 'usuario_cambio', 
        'fecha_cambio'
    ]
    list_filter = ['activo', 'fecha_cambio']
    search_fields = [
        'puerta__nombre', 'puerta__ubicacion', 
        'usuario_cambio__username', 'observaciones'
    ]
    ordering = ['-fecha_cambio']
    readonly_fields = ['fecha_cambio']
    list_per_page = 20
    
    fieldsets = (
        ('Puerta y Estado', {
            'fields': ('puerta', 'activo')
        }),
        ('Información de Cambio', {
            'fields': ('usuario_cambio', 'observaciones', 'fecha_cambio')
        }),
    )
    
    actions = ['activar_seguro', 'desactivar_seguro']
    
    def activar_seguro(self, request, queryset):
        """Acción para activar seguros"""
        for seguro in queryset:
            seguro.activar(usuario=request.user, observacion="Activado desde admin")
        self.message_user(request, f'{queryset.count()} seguro(s) activado(s).')
    activar_seguro.short_description = "Activar seguros seleccionados"
    
    def desactivar_seguro(self, request, queryset):
        """Acción para desactivar seguros"""
        for seguro in queryset:
            seguro.desactivar(usuario=request.user, observacion="Desactivado desde admin")
        self.message_user(request, f'{queryset.count()} seguro(s) desactivado(s).')
    desactivar_seguro.short_description = "Desactivar seguros seleccionados"
