from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
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
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol', 'cambiar_password_link')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'profile__rol')
    
    def get_rol(self, obj):
        """Mostrar el rol del perfil si existe"""
        try:
            return obj.profile.get_rol_display()
        except UserProfile.DoesNotExist:
            return '-'
    get_rol.short_description = 'Rol'
    get_rol.admin_order_field = 'profile__rol'
    
    def cambiar_password_link(self, obj):
        """Enlace para cambiar contraseña (siempre visible, permisos se validan en la URL)"""
        url = reverse('admin:auth_user_password_change', args=[obj.pk])
        return format_html('<a href="{}">🔑 Cambiar contraseña</a>', url)
    
    def get_readonly_fields(self, request, obj=None):
        """Control de campos según el rol del usuario actual"""
        readonly = list(super().get_readonly_fields(request, obj))
        
        # Si no es superusuario, verificar permisos por rol
        if not request.user.is_superuser:
            try:
                profile = request.user.profile
                
                # MAESTRO no puede editar is_superuser, is_staff, groups, user_permissions
                if profile.rol == 'MAESTRO':
                    readonly.extend(['is_superuser', 'is_staff', 'groups', 'user_permissions'])
                
                # ALUMNO no puede acceder al admin (se maneja en has_view_permission)
                
            except UserProfile.DoesNotExist:
                # Si no tiene perfil, solo puede ver campos básicos
                readonly.extend(['is_superuser', 'is_staff', 'groups', 'user_permissions'])
        
        return readonly
    
    def has_view_permission(self, request, obj=None):
        """Control de visualización según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # ADMIN, DIRECTOR y MAESTRO pueden ver usuarios
            return profile.puede_gestionar_usuarios()
        except UserProfile.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        """Control de edición según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # ADMIN, DIRECTOR y MAESTRO pueden editar usuarios
            return profile.puede_gestionar_usuarios()
        except UserProfile.DoesNotExist:
            return False
    
    def has_add_permission(self, request):
        """Control de creación según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # Solo ADMIN y DIRECTOR pueden crear usuarios
            return profile.rol in ['ADMIN', 'DIRECTOR'] and profile.activo
        except UserProfile.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        """Control de eliminación según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # Solo ADMIN puede eliminar usuarios
            return profile.rol == 'ADMIN' and profile.activo
        except UserProfile.DoesNotExist:
            return False


# Guardar request en el admin site para usar en métodos de instancia
class AdminSite(admin.AdminSite):
    def each_context(self, request):
        self._request = request
        return super().each_context(request)

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
        'activo', 'fecha_creacion', 'cambiar_password_usuario'
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
    
    def cambiar_password_usuario(self, obj):
        """Enlace para cambiar contraseña del usuario"""
        url = reverse('admin:auth_user_password_change', args=[obj.user.pk])
        return format_html('<a href="{}">🔑 Cambiar contraseña</a>', url)
    cambiar_password_usuario.short_description = 'Contraseña'
    
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
        Control de campos según el rol del usuario actual
        """
        readonly = list(self.readonly_fields)
        
        if not request.user.is_superuser:
            try:
                profile = request.user.profile
                
                # MAESTRO puede ver pero no modificar código de acceso
                if profile.rol == 'MAESTRO':
                    readonly.append('codigo_acceso')
                
                # DIRECTOR y ADMIN pueden editar código de acceso
                
            except UserProfile.DoesNotExist:
                readonly.append('codigo_acceso')
        
        return readonly
    
    def has_view_permission(self, request, obj=None):
        """Control de visualización según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # ADMIN, DIRECTOR y MAESTRO pueden ver perfiles
            return profile.puede_gestionar_usuarios()
        except UserProfile.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        """Control de edición según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # ADMIN, DIRECTOR y MAESTRO pueden editar perfiles
            return profile.puede_gestionar_usuarios()
        except UserProfile.DoesNotExist:
            return False
    
    def has_add_permission(self, request):
        """Control de creación según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # Solo ADMIN y DIRECTOR pueden crear perfiles
            return profile.rol in ['ADMIN', 'DIRECTOR'] and profile.activo
        except UserProfile.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        """Control de eliminación según rol"""
        if request.user.is_superuser:
            return True
        
        try:
            profile = request.user.profile
            # Solo ADMIN puede eliminar perfiles
            return profile.rol == 'ADMIN' and profile.activo
        except UserProfile.DoesNotExist:
            return False


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
