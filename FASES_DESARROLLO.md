# 📋 Fases de Desarrollo - Sistema de Control de Accesos

Este documento define las fases cortas y estructuradas para el desarrollo del sistema de control de accesos. Cada fase está diseñada para ser completada de manera incremental, con commits frecuentes en Git para asegurar el trabajo y permitir rollbacks si es necesario.

---

## 🎯 Metodología de Trabajo

- ✅ Completar cada fase antes de pasar a la siguiente
- 💾 Hacer commit al finalizar cada tarea importante
- 🧪 Probar funcionalidad antes de hacer commit
- 📝 Usar mensajes de commit descriptivos
- 🔄 Hacer rollback si algo no funciona correctamente

---

## 📦 FASE 0: Preparación del Entorno

**Objetivo:** Configurar el entorno de desarrollo y estructura base del proyecto.

### Tareas:
- [ ] Inicializar repositorio Git
  - Comando: `git init`
  - Commit: "Initial commit - Project structure"
  
- [ ] Crear `.gitignore` para Python/Django
  - Ignorar: `*.pyc`, `__pycache__/`, `venv/`, `.env`, `db.sqlite3`, `media/`, `.vscode/`
  - Commit: "Add .gitignore file"

- [ ] Crear entorno virtual Python
  - Comando: `python -m venv venv`
  - Activar: `source venv/bin/activate`

- [ ] Crear `requirements.txt` base
  - Django==5.0.0
  - djangorestframework==3.14.0
  - mysqlclient==2.2.0
  - djangorestframework-simplejwt==5.3.0
  - Pillow==10.1.0
  - python-dotenv==1.0.0
  - Commit: "Add initial requirements.txt"

- [ ] Crear archivo `.env.example` con variables de entorno
  - Commit: "Add .env.example template"

---

## 📦 FASE 1: Configuración Inicial de Django

**Objetivo:** Crear y configurar el proyecto Django base.

### Tareas:
- [ ] Crear proyecto Django
  - Comando: `django-admin startproject smart_access_backend`
  - Commit: "Create Django project structure"

- [ ] Configurar `settings.py`
  - Configurar MySQL como base de datos
  - Agregar `rest_framework` a `INSTALLED_APPS`
  - Configurar `MEDIA_ROOT` y `MEDIA_URL`
  - Configurar zona horaria y lenguaje
  - Commit: "Configure Django settings for MySQL and media files"

- [ ] Crear base de datos MySQL
  - Comando: `CREATE DATABASE control_accesos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
  - Documentar en README.md

- [ ] Ejecutar migraciones iniciales
  - Comando: `python manage.py migrate`
  - Commit: "Run initial migrations"

- [ ] Crear superusuario
  - Comando: `python manage.py createsuperuser`
  - Documentar credenciales en lugar seguro (NO en Git)

- [ ] Verificar que el servidor funciona
  - Comando: `python manage.py runserver`
  - Commit: "Verify Django server functionality"

---

## 📦 FASE 2: App de Control de Accesos (Modelos Base)

**Objetivo:** Crear la app principal y definir modelos de usuarios y roles.

### Tareas:
- [ ] Crear app `access_control`
  - Comando: `python manage.py startapp access_control`
  - Agregar a `INSTALLED_APPS`
  - Commit: "Create access_control app"

- [ ] Crear modelo `UserProfile` (extender User de Django)
  - Campos: rol, código_acceso, teléfono, activo
  - Choices para roles: ADMIN, DIRECTOR, MAESTRO, ALUMNO
  - Commit: "Add UserProfile model with roles"

- [ ] Crear modelo `Door` (Puerta)
  - Campos: nombre, ubicación, estado (abierta/cerrada), descripción
  - Commit: "Add Door model"

- [ ] Crear modelo `LockState` (Estado del Seguro)
  - Campos: puerta (FK), activo, fecha_cambio, usuario_cambio
  - Commit: "Add LockState model"

- [ ] Hacer migraciones y aplicarlas
  - Comando: `python manage.py makemigrations`
  - Comando: `python manage.py migrate`
  - Commit: "Create and apply access_control migrations"

- [ ] Registrar modelos en `admin.py`
  - Commit: "Register models in Django admin"

---

## 📦 FASE 3: App de Auditoría (Registros de Acceso)

**Objetivo:** Crear sistema de registro de intentos de acceso con fotografías.

### Tareas:
- [ ] Crear app `audit`
  - Comando: `python manage.py startapp audit`
  - Agregar a `INSTALLED_APPS`
  - Commit: "Create audit app"

- [ ] Crear modelo `AccessAttempt`
  - Campos: usuario, puerta, fecha_hora, exitoso, código_usado, imagen, ip_address
  - Commit: "Add AccessAttempt model with image field"

- [ ] Configurar upload de imágenes
  - Configurar función para nombrado de archivos
  - Configurar path: `media/access_attempts/{year}/{month}/{day}/`
  - Commit: "Configure image upload paths for access attempts"

- [ ] Hacer migraciones y aplicarlas
  - Commit: "Create and apply audit migrations"

- [ ] Registrar modelos en `admin.py` con preview de imágenes
  - Commit: "Register audit models in admin with image preview"

---

## 📦 FASE 4: API REST - Endpoints Básicos

**Objetivo:** Crear los primeros endpoints de la API REST.

### Tareas:
- [ ] Configurar Django REST Framework en `settings.py`
  - Configurar autenticación JWT
  - Configurar permisos por defecto
  - Commit: "Configure DRF with JWT authentication"

- [ ] Crear serializers en `access_control`
  - UserSerializer
  - DoorSerializer
  - LockStateSerializer
  - Commit: "Add serializers for access_control models"

- [ ] Crear viewsets básicos
  - UserViewSet
  - DoorViewSet
  - Commit: "Add basic viewsets for users and doors"

- [ ] Configurar URLs de la API
  - Crear `api/urls.py`
  - Registrar rutas en router
  - Commit: "Configure API URLs with router"

- [ ] Probar endpoints con Postman/Thunder Client
  - Documentar ejemplos en README.md
  - Commit: "Test and document basic API endpoints"

---

## 📦 FASE 5: API REST - Registro de Accesos

**Objetivo:** Implementar endpoint para registrar intentos de acceso.

### Tareas:
- [ ] Crear serializer para `AccessAttempt`
  - Incluir validación de imagen
  - Commit: "Add AccessAttempt serializer with image validation"

- [ ] Crear vista para registrar intento de acceso
  - POST `/api/access/attempt/`
  - Validar código
  - Verificar estado del seguro
  - Guardar imagen
  - Registrar resultado
  - Commit: "Implement access attempt registration endpoint"

- [ ] Crear vista para listar registros de acceso
  - GET `/api/access/logs/`
  - Filtrar por fecha, usuario, resultado
  - Paginación
  - Commit: "Add access logs listing endpoint with filters"

- [ ] Crear vista para obtener imagen de acceso
  - GET `/api/access/image/<id>/`
  - Restricción solo para admin
  - Commit: "Add endpoint to retrieve access attempt images"

- [ ] Probar flujo completo de registro
  - Commit: "Test complete access attempt flow"

---

## 📦 FASE 6: Control de Puertas y Seguros

**Objetivo:** Implementar control de estado de puertas y seguros.

### Tareas:
- [ ] Crear endpoint para abrir/cerrar puerta
  - POST `/api/door/open/`
  - POST `/api/door/close/`
  - Validar permisos por rol
  - Commit: "Implement door open/close endpoints with role validation"

- [ ] Crear endpoint para activar/desactivar seguro
  - POST `/api/door/lock/`
  - POST `/api/door/unlock/`
  - Validar que solo Director+ puede desactivar
  - Commit: "Implement lock control with role-based permissions"

- [ ] Crear endpoint para consultar estado
  - GET `/api/door/status/<id>/`
  - Retornar: estado puerta, estado seguro, último acceso
  - Commit: "Add door status query endpoint"

- [ ] Crear lógica de validación de acceso según seguro
  - Integrar con AccessAttempt
  - Commit: "Integrate lock state validation in access attempts"

- [ ] Probar todos los escenarios de permisos
  - Commit: "Test all permission scenarios for door control"

---

## 📦 FASE 7: Sistema de Autenticación JWT

**Objetivo:** Implementar autenticación completa con JWT.

### Tareas:
- [ ] Configurar endpoints de autenticación
  - POST `/api/auth/login/`
  - POST `/api/auth/logout/`
  - POST `/api/auth/refresh/`
  - Commit: "Add JWT authentication endpoints"

- [ ] Crear serializer de login personalizado
  - Retornar información del usuario y su rol
  - Commit: "Add custom login serializer with user role"

- [ ] Implementar permisos personalizados por rol
  - `IsAdmin`, `IsDirectorOrAbove`, `IsMaestroOrAbove`
  - Commit: "Implement custom role-based permissions"

- [ ] Aplicar permisos a todos los endpoints
  - Commit: "Apply role-based permissions to all endpoints"

- [ ] Probar autenticación completa
  - Commit: "Test complete JWT authentication flow"

---

## 📦 FASE 8: Frontend Base - Dashboard

**Objetivo:** Crear interfaz web básica para el dashboard.

### Tareas:
- [ ] Crear estructura de directorios frontend
  - `frontend/templates/`, `frontend/static/`
  - Commit: "Create frontend directory structure"

- [ ] Crear template base con Bootstrap 5
  - `base.html` con navbar y estructura
  - Commit: "Add base template with Bootstrap 5"

- [ ] Crear página de login
  - `login.html` con formulario
  - JavaScript para autenticación JWT
  - Commit: "Implement login page with JWT authentication"

- [ ] Crear dashboard principal
  - `dashboard.html`
  - Mostrar estado de puertas
  - Botones de control según rol
  - Commit: "Create main dashboard with door status"

- [ ] Crear página de registros de acceso
  - Tabla con filtros
  - Modal para ver imágenes
  - Commit: "Add access logs page with image modal"

- [ ] Integrar JavaScript para llamadas a API
  - Fetch API o Axios
  - Manejo de tokens JWT
  - Commit: "Implement JavaScript API client with JWT handling"

---

## 📦 FASE 9: Gestión de Usuarios (Frontend)

**Objetivo:** Crear interfaz para gestión de usuarios.

### Tareas:
- [ ] Crear página de lista de usuarios
  - Tabla con búsqueda y filtros
  - Commit: "Add user list page with search"

- [ ] Crear formulario de creación de usuario
  - Validación de campos
  - Asignación de rol
  - Commit: "Implement user creation form"

- [ ] Crear formulario de edición de usuario
  - Pre-cargar datos existentes
  - Commit: "Add user edit form with data preload"

- [ ] Implementar activar/desactivar usuarios
  - Toggle de estado
  - Commit: "Add user activation/deactivation toggle"

- [ ] Probar flujo completo de gestión
  - Commit: "Test complete user management flow"

---

## 📦 FASE 10: Integración IoT - Preparación Backend

**Objetivo:** Preparar backend para recibir datos del ESP32.

### Tareas:
- [ ] Crear endpoint para registro de dispositivo IoT
  - POST `/api/iot/register/`
  - Commit: "Add IoT device registration endpoint"

- [ ] Crear modelo `IoTDevice`
  - Campos: identificador, nombre, puerta_asignada, activo
  - Commit: "Add IoTDevice model"

- [ ] Modificar endpoint de intento de acceso
  - Aceptar device_id
  - Validar dispositivo registrado
  - Commit: "Update access attempt endpoint for IoT devices"

- [ ] Crear endpoint para recibir estado del ESP32
  - POST `/api/iot/status/`
  - Commit: "Add endpoint to receive ESP32 status updates"

- [ ] Documentar formato de comunicación IoT
  - JSON schema esperado
  - Commit: "Document IoT communication format"

---

## 📦 FASE 11: Testing y Validación

**Objetivo:** Crear tests unitarios y de integración.

### Tareas:
- [ ] Configurar framework de testing
  - pytest-django o unittest
  - Commit: "Configure testing framework"

- [ ] Crear tests para modelos
  - Validaciones de UserProfile
  - Estados de Door y LockState
  - Commit: "Add model tests"

- [ ] Crear tests para endpoints de acceso
  - Intentos exitosos y fallidos
  - Validación de permisos
  - Commit: "Add access attempt endpoint tests"

- [ ] Crear tests para control de puertas
  - Permisos por rol
  - Estados del seguro
  - Commit: "Add door control tests"

- [ ] Ejecutar todos los tests
  - Comando: `python manage.py test`
  - Commit: "Run and verify all tests pass"

---

## 📦 FASE 12: Documentación y Despliegue

**Objetivo:** Documentar el sistema y preparar para despliegue.

### Tareas:
- [ ] Generar documentación de API con Swagger
  - Instalar drf-yasg
  - Configurar URLs
  - Commit: "Add Swagger API documentation"

- [ ] Crear guía de instalación detallada
  - Actualizar README.md
  - Incluir configuración de MySQL
  - Commit: "Update installation guide in README"

- [ ] Crear scripts de deployment
  - Script de setup inicial
  - Script de backup de base de datos
  - Commit: "Add deployment and backup scripts"

- [ ] Configurar variables de entorno para producción
  - DEBUG=False
  - ALLOWED_HOSTS
  - SECRET_KEY segura
  - Commit: "Configure production environment variables"

- [ ] Crear guía de uso para usuarios finales
  - Manual de administrador
  - Manual de usuario
  - Commit: "Add user manuals"

---

## 📦 FASE 13 (Opcional): Mejoras Avanzadas

**Objetivo:** Implementar funcionalidades adicionales.

### Tareas:
- [ ] Implementar notificaciones en tiempo real
  - WebSocket con Django Channels
  - Commit: "Add real-time notifications with WebSockets"

- [ ] Agregar módulo de reportes
  - Exportar a PDF
  - Exportar a Excel
  - Commit: "Implement report export functionality"

- [ ] Implementar reconocimiento facial básico
  - OpenCV para detección de rostros
  - Commit: "Add basic facial recognition"

- [ ] Crear modo offline para ESP32
  - Cache local de intentos
  - Sincronización posterior
  - Commit: "Implement offline mode for IoT devices"

- [ ] Agregar logs de auditoría del sistema
  - Registrar cambios en configuración
  - Commit: "Add system audit logs"

---

## 📋 Convenciones de Commits

Usa prefijos descriptivos para tus commits:

- **feat:** Nueva funcionalidad
- **fix:** Corrección de bugs
- **docs:** Cambios en documentación
- **style:** Cambios de formato (no afectan código)
- **refactor:** Refactorización de código
- **test:** Agregar o modificar tests
- **chore:** Tareas de mantenimiento

**Ejemplos:**
```bash
git commit -m "feat: Add UserProfile model with role-based permissions"
git commit -m "fix: Correct lock state validation logic"
git commit -m "docs: Update API endpoints documentation"
git commit -m "test: Add unit tests for access attempt validation"
```

---

## 🔄 Workflow de Desarrollo

1. **Antes de empezar una fase:**
   ```bash
   git status  # Verificar que no hay cambios sin commit
   git pull    # Actualizar con cambios remotos (si aplica)
   ```

2. **Durante el desarrollo:**
   - Hacer commits pequeños y frecuentes
   - Probar cada cambio antes de hacer commit
   - Escribir mensajes descriptivos

3. **Al completar una fase:**
   ```bash
   git add .
   git commit -m "feat: Complete Phase X - [Description]"
   git push origin main  # Si usas repositorio remoto
   ```

4. **Si algo sale mal:**
   ```bash
   git log --oneline  # Ver historial de commits
   git checkout [commit-hash] -- [file]  # Restaurar archivo específico
   git revert [commit-hash]  # Revertir commit completo
   git reset --hard [commit-hash]  # Volver a estado anterior (¡cuidado!)
   ```

---

## ✅ Checklist de Finalización de Fase

Antes de marcar una fase como completada, verifica:

- [ ] ✅ Código funciona correctamente
- [ ] ✅ Commits realizados con mensajes descriptivos
- [ ] ✅ No hay errores en consola
- [ ] ✅ Documentación actualizada si corresponde
- [ ] ✅ Tests pasan (si aplica)
- [ ] ✅ Cambios pusheados a repositorio remoto (si aplica)

---

**Fecha de inicio:** [Registrar fecha]  
**Última actualización:** 15 de octubre de 2025  
**Responsable:** Perseo de Jesús Osuna Padierna
