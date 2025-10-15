"""
Management command para limpiar todos los datos de prueba del sistema.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from access_control.models import UserProfile, Door, LockState


class Command(BaseCommand):
    help = 'Elimina todos los datos de prueba del sistema (excepto superusuario admin)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirmar que deseas eliminar los datos',
        )

    def handle(self, *args, **kwargs):
        confirmar = kwargs.get('confirmar', False)
        
        if not confirmar:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ADVERTENCIA: Este comando eliminará TODOS los datos de prueba.\n'
                    '   Para continuar, ejecuta: python manage.py limpiar_datos --confirmar'
                )
            )
            return
        
        self.stdout.write(self.style.WARNING('🗑️  Iniciando limpieza de datos de prueba...\n'))
        
        # Contar datos antes de eliminar
        usuarios_count = User.objects.exclude(username='admin').count()
        perfiles_count = UserProfile.objects.exclude(user__username='admin').count()
        puertas_count = Door.objects.count()
        seguros_count = LockState.objects.count()
        
        self.stdout.write(f'📊 Datos actuales:')
        self.stdout.write(f'   Usuarios (sin admin): {usuarios_count}')
        self.stdout.write(f'   Perfiles (sin admin): {perfiles_count}')
        self.stdout.write(f'   Puertas: {puertas_count}')
        self.stdout.write(f'   Seguros: {seguros_count}\n')
        
        # Eliminar seguros
        self.stdout.write('🔐 Eliminando estados de seguros...')
        LockState.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('   ✅ Seguros eliminados'))
        
        # Eliminar puertas
        self.stdout.write('🚪 Eliminando puertas...')
        Door.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('   ✅ Puertas eliminadas'))
        
        # Eliminar perfiles (excepto admin)
        self.stdout.write('👤 Eliminando perfiles de usuario (excepto admin)...')
        UserProfile.objects.exclude(user__username='admin').delete()
        self.stdout.write(self.style.SUCCESS('   ✅ Perfiles eliminados'))
        
        # Eliminar usuarios (excepto admin)
        self.stdout.write('🗑️  Eliminando usuarios (excepto admin)...')
        User.objects.exclude(username='admin').delete()
        self.stdout.write(self.style.SUCCESS('   ✅ Usuarios eliminados'))
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✨ Limpieza completada exitosamente\n'))
        
        self.stdout.write('📊 Estado final:')
        self.stdout.write(f'   Usuarios: {User.objects.count()} (solo admin)')
        self.stdout.write(f'   Perfiles: {UserProfile.objects.count()}')
        self.stdout.write(f'   Puertas: {Door.objects.count()}')
        self.stdout.write(f'   Seguros: {LockState.objects.count()}')
        
        self.stdout.write('\n💡 Ahora puedes crear usuarios limpios desde el admin.')
        self.stdout.write('   http://127.0.0.1:8000/admin/auth/user/add/')
        self.stdout.write('='*50 + '\n')
