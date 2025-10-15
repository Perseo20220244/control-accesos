"""
Signals para la app access_control.
Gestión automática de perfiles de usuario.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente un UserProfile cuando se crea un nuevo User.
    Si el usuario ya tiene perfil, no hace nada.
    """
    if created:
        # Solo crear perfil si no existe
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(
                user=instance,
                rol='ALUMNO',  # Rol por defecto
                codigo_acceso=f'temp_{instance.id}',  # Temporal, debe cambiarse
                activo=True
            )


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Guarda el perfil del usuario cuando se guarda el User.
    """
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        # Si no existe el perfil, crearlo
        UserProfile.objects.create(
            user=instance,
            rol='ALUMNO',
            codigo_acceso=f'temp_{instance.id}',
            activo=True
        )
