from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    """
    Perfil extendido del usuario con información de control de acceso.
    Roles: ADMIN, DIRECTOR, MAESTRO, ALUMNO
    """
    
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('DIRECTOR', 'Director'),
        ('MAESTRO', 'Maestro'),
        ('ALUMNO', 'Alumno'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    
    rol = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='ALUMNO',
        verbose_name='Rol'
    )
    
    codigo_acceso = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]+$',
                message='El código de acceso solo puede contener números',
            )
        ],
        verbose_name='Código de Acceso',
        help_text='Código numérico para acceso físico'
    )
    
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Número de teléfono debe tener entre 9 y 15 dígitos',
            )
        ],
        verbose_name='Teléfono'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Usuario puede acceder al sistema'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_rol_display()}"
    
    def puede_abrir_puerta(self):
        """Todos los roles pueden abrir puertas"""
        return self.activo
    
    def puede_gestionar_usuarios(self):
        """Director, Maestro y Admin pueden gestionar usuarios"""
        return self.rol in ['ADMIN', 'DIRECTOR', 'MAESTRO'] and self.activo
    
    def puede_controlar_seguro(self):
        """Director, Maestro y Admin pueden controlar el seguro"""
        return self.rol in ['ADMIN', 'DIRECTOR', 'MAESTRO'] and self.activo
    
    def puede_desactivar_seguro(self):
        """Solo Director y Admin pueden desactivar seguro principal"""
        return self.rol in ['ADMIN', 'DIRECTOR'] and self.activo


class Door(models.Model):
    """
    Modelo para representar las puertas del sistema.
    """
    
    ESTADO_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre',
        help_text='Nombre identificador de la puerta'
    )
    
    ubicacion = models.CharField(
        max_length=200,
        verbose_name='Ubicación',
        help_text='Ubicación física de la puerta'
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='CERRADA',
        verbose_name='Estado Actual'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='La puerta está operativa'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Modificación'
    )
    
    class Meta:
        verbose_name = 'Puerta'
        verbose_name_plural = 'Puertas'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
    
    def abrir(self):
        """Cambia el estado a ABIERTA"""
        self.estado = 'ABIERTA'
        self.save()
    
    def cerrar(self):
        """Cambia el estado a CERRADA"""
        self.estado = 'CERRADA'
        self.save()


class LockState(models.Model):
    """
    Modelo para gestionar el estado del seguro de cada puerta.
    """
    
    puerta = models.OneToOneField(
        Door,
        on_delete=models.CASCADE,
        related_name='seguro',
        verbose_name='Puerta'
    )
    
    activo = models.BooleanField(
        default=False,
        verbose_name='Seguro Activo',
        help_text='Si está activo, solo usuarios autorizados pueden acceder'
    )
    
    fecha_cambio = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Último Cambio'
    )
    
    usuario_cambio = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_seguro',
        verbose_name='Usuario que Realizó el Cambio'
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones'
    )
    
    class Meta:
        verbose_name = 'Estado del Seguro'
        verbose_name_plural = 'Estados de Seguros'
        ordering = ['-fecha_cambio']
    
    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"Seguro {self.puerta.nombre}: {estado}"
    
    def activar(self, usuario=None, observacion=None):
        """Activa el seguro de la puerta"""
        self.activo = True
        self.usuario_cambio = usuario
        if observacion:
            self.observaciones = observacion
        self.save()
    
    def desactivar(self, usuario=None, observacion=None):
        """Desactiva el seguro de la puerta"""
        self.activo = False
        self.usuario_cambio = usuario
        if observacion:
            self.observaciones = observacion
        self.save()
