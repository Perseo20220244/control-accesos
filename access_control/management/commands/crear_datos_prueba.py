"""
Management command para crear datos de prueba en el sistema de control de accesos.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from access_control.models import UserProfile, Door, LockState


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de control de accesos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando creación de datos de prueba...'))
        
        # Crear usuarios de prueba
        self.stdout.write('📝 Creando usuarios...')
        
        # Crear usuario Director
        if not User.objects.filter(username='director').exists():
            user_director = User.objects.create_user(
                username='director',
                email='director@universidad.edu',
                password='director123',
                first_name='María',
                last_name='González Pérez'
            )
            UserProfile.objects.create(
                user=user_director,
                rol='DIRECTOR',
                codigo_acceso='1001',
                telefono='+526141234567',
                activo=True
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Director creado: director / director123'))
        
        # Crear usuario Maestro
        if not User.objects.filter(username='maestro').exists():
            user_maestro = User.objects.create_user(
                username='maestro',
                email='maestro@universidad.edu',
                password='maestro123',
                first_name='Carlos',
                last_name='Ramírez López'
            )
            UserProfile.objects.create(
                user=user_maestro,
                rol='MAESTRO',
                codigo_acceso='2001',
                telefono='+526142345678',
                activo=True
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Maestro creado: maestro / maestro123'))
        
        # Crear usuarios Alumnos
        alumnos_data = [
            ('juan.perez', 'Juan', 'Pérez', '3001'),
            ('ana.martinez', 'Ana', 'Martínez', '3002'),
            ('luis.garcia', 'Luis', 'García', '3003'),
            ('sofia.lopez', 'Sofía', 'López', '3004'),
        ]
        
        for username, first_name, last_name, codigo in alumnos_data:
            if not User.objects.filter(username=username).exists():
                user_alumno = User.objects.create_user(
                    username=username,
                    email=f'{username}@estudiantes.edu',
                    password='alumno123',
                    first_name=first_name,
                    last_name=last_name
                )
                UserProfile.objects.create(
                    user=user_alumno,
                    rol='ALUMNO',
                    codigo_acceso=codigo,
                    telefono=f'+52614{codigo}0000',
                    activo=True
                )
                self.stdout.write(self.style.SUCCESS(f'  ✅ Alumno creado: {username} / alumno123'))
        
        # Crear puertas
        self.stdout.write('\n🚪 Creando puertas...')
        
        puertas_data = [
            {
                'nombre': 'Laboratorio de Computación A',
                'ubicacion': 'Edificio Principal, Piso 2, Sala 201',
                'descripcion': 'Laboratorio equipado con 30 computadoras para clases de programación',
                'estado': 'CERRADA',
            },
            {
                'nombre': 'Laboratorio de Redes',
                'ubicacion': 'Edificio de Ingeniería, Piso 3, Sala 305',
                'descripcion': 'Laboratorio especializado en equipos de redes y telecomunicaciones',
                'estado': 'CERRADA',
            },
            {
                'nombre': 'Sala de Servidores',
                'ubicacion': 'Edificio Principal, Sótano, Sala S-01',
                'descripcion': 'Sala con servidores críticos del sistema universitario',
                'estado': 'CERRADA',
            },
            {
                'nombre': 'Biblioteca - Sala de Estudio',
                'ubicacion': 'Edificio Biblioteca, Piso 1, Sala A',
                'descripcion': 'Sala de estudio grupal con capacidad para 20 personas',
                'estado': 'ABIERTA',
            },
            {
                'nombre': 'Auditorio Principal',
                'ubicacion': 'Edificio Central, Planta Baja',
                'descripcion': 'Auditorio con capacidad para 200 personas',
                'estado': 'CERRADA',
            },
        ]
        
        for puerta_data in puertas_data:
            if not Door.objects.filter(nombre=puerta_data['nombre']).exists():
                puerta = Door.objects.create(**puerta_data)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Puerta creada: {puerta.nombre}'))
                
                # Crear estado del seguro para cada puerta
                # Solo las puertas críticas tienen seguro activado
                seguro_activo = puerta.nombre in ['Sala de Servidores', 'Laboratorio de Redes']
                
                LockState.objects.create(
                    puerta=puerta,
                    activo=seguro_activo,
                    usuario_cambio=User.objects.get(username='admin'),
                    observaciones='Configuración inicial del sistema'
                )
                
                estado_seguro = '🔐 Activado' if seguro_activo else '🔓 Desactivado'
                self.stdout.write(self.style.SUCCESS(f'     Seguro: {estado_seguro}'))
        
        # Resumen
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✨ Datos de prueba creados exitosamente\n'))
        
        self.stdout.write(self.style.WARNING('👥 CREDENCIALES DE ACCESO:'))
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Director: director / director123')
        self.stdout.write('  Maestro:  maestro / maestro123')
        self.stdout.write('  Alumnos:  [username] / alumno123')
        
        self.stdout.write('\n📊 RESUMEN:')
        self.stdout.write(f'  Usuarios: {UserProfile.objects.count()}')
        self.stdout.write(f'  Puertas:  {Door.objects.count()}')
        self.stdout.write(f'  Seguros:  {LockState.objects.count()}')
        
        self.stdout.write('\n🌐 Accede al admin en: http://127.0.0.1:8000/admin/')
        self.stdout.write('='*50 + '\n')
