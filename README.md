# 🏫 Sistema de Control de Accesos Inteligente para Entornos Educativos

## 📘 Descripción General

Este proyecto implementa un **sistema inteligente de control de accesos** para universidades, laboratorios y aulas con niveles de seguridad diferenciados.  
Está diseñado para integrarse con **dispositivos Ultraloq U-Bolt Pro (UB01)** y un **módulo IoT basado en ESP32**, permitiendo gestionar la autenticación, la apertura/cierre de puertas, la activación de seguros y la auditoría visual mediante fotografías tomadas en cada intento de acceso.

El objetivo principal es **garantizar que la persona que intenta acceder sea efectivamente la titular del código asignado**, previniendo el préstamo de contraseñas o identificadores.  
Cada intento (éxito o error) se registra junto con una **foto, fecha, hora, usuario y estado del seguro**.

---

## 🎯 Objetivos del Sistema

- Controlar accesos físicos mediante contraseñas y dispositivos IoT.
- Registrar intentos de acceso exitosos y fallidos con evidencia fotográfica.
- Identificar intentos de acceso no autorizados o suplantaciones.
- Permitir auditorías visuales por parte de administradores.
- Implementar jerarquías de usuarios con diferentes permisos de control.

---

## 🧠 Roles de Usuario

| Rol | Permisos |
|------|-----------|
| **Administrador** | - Acceso completo al sistema<br>- Ver y gestionar todas las fotos de auditoría<br>- Activar/desactivar el seguro principal<br>- Abrir/cerrar puertas<br>- Crear, editar y eliminar usuarios y contraseñas |
| **Director** | - Abrir/cerrar puerta<br>- Activar/desactivar el seguro<br>- Gestión completa de usuarios (crear, modificar, eliminar) |
| **Maestro** | - Gestión completa de usuarios<br>- Control del seguro<br>- Apertura/cierre de puerta |
| **Alumno** | - Abrir y cerrar puerta únicamente (si el seguro no está activado) |

> 🔒 Si el seguro principal está activado, **solo usuarios con nivel Director o superior** podrán desactivarlo.

---

## 🧩 Arquitectura del Sistema

El sistema se divide en tres capas principales:

### 1. Backend (Django + MySQL)
- API REST desarrollada con **Django Rest Framework (DRF)**.  
- Base de datos **MySQL** para el almacenamiento de:
  - Usuarios, roles y contraseñas.
  - Registros de acceso (fecha, hora, resultado, imagen).
  - Estado actual del seguro y de cada puerta.
- Autenticación y autorización basada en **JWT o Django Sessions**.
- Gestión de medios (fotografías) usando **Django Media Storage**.
- Panel de administración para visualizar registros e imágenes.

### 2. Dispositivos IoT (ESP32 + Ultraloq U-Bolt Pro)
- El **ESP32** actúa como intermediario entre el dispositivo físico y el backend:
  - Captura y envía fotografías del intento de acceso.
  - Lee el estado del seguro (activo/inactivo).
  - Recibe comandos para abrir o cerrar la puerta.
- Comunicación vía **HTTP REST API o MQTT** con el servidor Django.
- Configurable mediante conexión Wi-Fi local o red institucional.

### 3. Interfaz de Usuario (Web)
- Panel web responsive (Bootstrap 5 + JS).
- Dashboard con:
  - Estado en tiempo real de la puerta y el seguro.
  - Tabla de registros de acceso (foto, usuario, resultado, fecha/hora).
  - Botones para abrir/cerrar o activar/desactivar el seguro (según permisos).
- Visualización restringida de fotografías solo para roles autorizados.

---

## 📷 Flujo de Acceso

1. El usuario ingresa su **código en el dispositivo Ultraloq**.  
2. El dispositivo (vía ESP32) **captura una foto** y la envía al backend con el intento.  
3. El backend **verifica la validez del código y el estado del seguro**.  
4. El sistema registra el intento con:
   - ID del usuario (si coincide),
   - fecha/hora,
   - resultado (éxito/fallo),
   - imagen capturada.  
5. Si el acceso es válido y el seguro está desactivado, la puerta se abre.  
6. El administrador puede **auditar las fotos** desde el panel web.

---

## 🧱 Estructura del Proyecto (propuesta)

```
smart_access_system/
│
├── backend/
│   ├── manage.py
│   ├── smart_access_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── access_control/       # app principal (usuarios, roles, puertas, seguros)
│   ├── audit/                # app para registros de acceso y fotos
│   └── api/                  # endpoints REST
│
├── frontend/
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── esp32/
│   ├── main.cpp              # firmware para conexión WiFi + HTTP POST
│   ├── camera_capture.h
│   └── wifi_config.h
│
└── README.md
```

---

## 🔐 Funcionalidades Clave

- [x] Registro fotográfico de cada intento de acceso.  
- [x] Control de estados (puerta abierta/cerrada, seguro activo/inactivo).  
- [x] Gestión de usuarios y roles.  
- [x] API REST segura (autenticación JWT).  
- [x] Integración IoT (ESP32).  
- [x] Auditoría visual completa para administradores.

---

## 🚀 Tecnologías Principales

| Componente | Tecnología |
|-------------|-------------|
| Backend | Django + Django Rest Framework |
| Base de datos | MySQL |
| Comunicación IoT | HTTP / MQTT + JSON |
| Microcontrolador | ESP32 (C++ / Arduino Core) |
| Dispositivo físico | Ultraloq U-Bolt Pro UB01 |
| Frontend | HTML, Bootstrap 5, JavaScript |
| Autenticación | JWT o Django Auth |
| Almacenamiento multimedia | Django Media (configurable para S3/local) |

---

## 💡 Sugerencias de Mejora

1. **Reconocimiento facial opcional** usando TensorFlow Lite o servicios externos para validar visualmente coincidencias entre foto actual y registro del usuario.
2. **Notificaciones en tiempo real** (WebSocket o MQTT) cuando haya intentos fallidos.
3. **Registro geográfico** del acceso si el dispositivo IoT dispone de GPS o red local diferenciada.
4. **Módulo de reportes** (PDF o Excel) para auditorías históricas.
5. **Soporte offline**: el ESP32 almacena temporalmente intentos cuando no hay conexión al servidor.
6. **Logs cifrados** y cifrado de imágenes para garantizar privacidad.
7. **Módulo de mantenimiento** que registre los cambios físicos o reinicios de los dispositivos.

---

## 🧰 Requisitos del Sistema

### 💻 **Software (Desarrollo)**
- **Python 3.11+** (https://python.org)
- **Git** (https://git-scm.com)

### 🪟 **Windows Específico**
- **XAMPP** (Apache + MySQL) - https://www.apachefriends.org/
- **Visual C++ Build Tools** - para compilar mysqlclient
- **PowerShell o Command Prompt**

### 🐧 **Linux/Mac**
- **MySQL Server 8.x** o **MariaDB**
- **Python dev headers**: `python3-dev`
- **MySQL dev headers**: `default-libmysqlclient-dev`

### 📦 **Dependencias Python** (instaladas automáticamente)
- **Django 5.0.0** - Framework web
- **djangorestframework 3.14.0** - API REST
- **djangorestframework-simplejwt 5.3.0** - Autenticación JWT
- **mysqlclient 2.2.0** - Conector MySQL
- **django-cors-headers** - CORS para API
- **Pillow 10.1.0** - Manejo de imágenes
- **python-dotenv** - Variables de entorno

### 🔌 **Hardware IoT** (Futuro)
- **ESP32** con cámara (AI-Thinker ESP32-CAM o M5Camera)
- **Ultraloq U-Bolt Pro UB01** - Cerradura inteligente
- **Conexión Wi-Fi** estable
- **Fuente de alimentación** para ESP32

### 🌐 **Navegadores Soportados**
- **Chrome 90+**, **Firefox 88+**, **Safari 14+**, **Edge 90+**

---

## ⚙️ Instalación del Sistema

### 🪟 Instalación en Windows

#### 1️⃣ **Requisitos Previos**
```powershell
# Verificar versión de Python (requiere 3.11+)
python --version

# Si no tienes Python, descargar desde: https://python.org
# Asegurar marcar "Add Python to PATH" durante instalación
```

#### 2️⃣ **Instalar XAMPP (MySQL)**
1. Descargar XAMPP desde: https://www.apachefriends.org/
2. Instalar con componentes: **Apache** y **MySQL**
3. Iniciar **XAMPP Control Panel**
4. **Iniciar** servicios **Apache** y **MySQL**
5. Crear base de datos:
   ```sql
   # Abrir phpMyAdmin (http://localhost/phpmyadmin)
   # Crear nueva base de datos: 'control_accesos'
   ```

#### 3️⃣ **Instalar Dependencias del Sistema**
```powershell
# Instalar Visual C++ Build Tools (necesario para mysqlclient)
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# O instalar Visual Studio Community con "C++ build tools"

# Alternativa: usar wheel precompilado
pip install wheel
```

#### 4️⃣ **Clonar y Configurar Proyecto**
```powershell
# Clonar repositorio
git clone https://github.com/Perseo20220244/control-accesos.git
cd control-accesos

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Verificar activación (debe aparecer (venv) en el prompt)
```

#### 5️⃣ **Instalar Dependencias Python**
```powershell
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Si mysqlclient falla, usar alternativa:
pip install pymysql
```

#### 6️⃣ **Configurar Variables de Entorno**
```powershell
# Copiar archivo de configuración
copy .env.example .env

# Editar .env con tus datos:
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_NAME=control_accesos
# DB_USER=root
# DB_PASSWORD=   (dejar vacío si no configuraste password en XAMPP)
```

#### 7️⃣ **Configurar Base de Datos**
```powershell
# Aplicar migraciones
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser
# Username: admin
# Email: tu-email@example.com
# Password: admin123 (o tu preferencia)
```

#### 8️⃣ **Ejecutar Servidor**
```powershell
# Iniciar servidor de desarrollo
python manage.py runserver

# Acceder a:
# Admin: http://127.0.0.1:8000/admin/
# Sistema: http://127.0.0.1:8000/
```

#### 9️⃣ **Solución de Problemas Comunes en Windows**

**Error mysqlclient:**
```powershell
# Instalar desde wheel precompilado
pip install https://download.lfd.uci.edu/pythonlibs/archived/mysqlclient-2.2.0-cp311-cp311-win_amd64.whl

# O usar PyMySQL como alternativa
pip install pymysql
# Agregar al inicio de settings.py:
# import pymysql
# pymysql.install_as_MySQLdb()
```

**Error de permisos:**
```powershell
# Ejecutar PowerShell como Administrador
# O usar Command Prompt (cmd) normal
```

**Error de encoding:**
```powershell
# Configurar encoding UTF-8
set PYTHONIOENCODING=utf-8
chcp 65001
```

---

### 🐧 Instalación en Linux/Mac

```bash
# Clonar repositorio
git clone https://github.com/Perseo20220244/control-accesos.git
cd control-accesos

# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus datos

# Migraciones y superusuario
python manage.py migrate
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

### ✅ Verificación de Instalación Correcta

#### **1. Verificar Servidor Django**
```powershell
# El servidor debe iniciar sin errores
python manage.py runserver

# Debes ver:
# ✅ Watching for file changes with StatReloader
# ✅ Performing system checks...
# ✅ System check identified no issues (0 silenced).
# ✅ Starting development server at http://127.0.0.1:8000/
```

#### **2. Probar Conexión a Base de Datos**
```powershell
# Verificar conexión MySQL
python manage.py dbshell

# Debe conectar a MySQL sin errores
# mysql> SELECT VERSION();
# mysql> SHOW DATABASES;
# mysql> exit;
```

#### **3. Acceder al Panel de Administración**
1. Ir a: http://127.0.0.1:8000/admin/
2. Iniciar sesión con el superuseradmin creado
3. Debes ver las siguientes secciones:
   - **👥 AUTHENTICATION AND AUTHORIZATION**
     - Users (con enlace 🔑 Cambiar contraseña)
   - **🏫 ACCESS_CONTROL** 
     - Perfiles de Usuarios
     - Puertas  
     - Estados de Seguros

#### **4. Probar Funcionalidades Clave**
- ✅ **Crear Usuario**: Admin → Users → Add user
- ✅ **Ver Perfil**: El perfil se crea automáticamente
- ✅ **Cambiar Contraseña**: Click en enlace �
- ✅ **Crear Puerta**: Access Control → Puertas → Add
- ✅ **Ver Permisos**: Según tu rol (Admin/Director/Maestro)

#### **5. Comandos de Gestión Disponibles**
```powershell
# Ver comandos personalizados
python manage.py help

# Crear datos de prueba
python manage.py crear_datos_prueba

# Limpiar datos de prueba  
python manage.py limpiar_datos --confirmar

# Ver usuarios actuales
python manage.py shell -c "from django.contrib.auth.models import User; print(f'Usuarios: {User.objects.count()}')"
```

---

### �🗂️ Estructura de Archivos Generados

```
control-accesos/
├── manage.py                    # Script principal Django
├── requirements.txt             # Dependencias Python  
├── .env.example                # Plantilla de configuración
├── .env                        # Configuración local (crear)
├── README.md                   # Este archivo
├── FASES_DESARROLLO.md         # Guía de desarrollo
├── PERMISOS_POR_ROL.md         # Matriz de permisos
├── smart_access_backend/       # Configuración Django
│   ├── settings.py             # Configuración principal
│   ├── urls.py                 # URLs del proyecto
│   └── wsgi.py                 # Servidor WSGI
├── access_control/             # App principal
│   ├── models.py               # Modelos de datos
│   ├── admin.py                # Panel administración
│   ├── views.py                # Vistas del sistema
│   ├── signals.py              # Señales automáticas
│   └── management/commands/    # Comandos personalizados
│       ├── crear_datos_prueba.py
│       └── limpiar_datos.py
└── venv/                       # Entorno virtual (crear)
```

---

### 🆘 Soporte y Solución de Problemas

#### **Errores Comunes en Windows**

**❌ 'python' no se reconoce como comando**
```powershell
# Solución: Reinstalar Python marcando "Add to PATH"
# O agregar manualmente: C:\Python311\;C:\Python311\Scripts\
```

**❌ Error al instalar mysqlclient**
```powershell
# Opción 1: Instalar Visual C++ Build Tools
# Opción 2: Usar wheel precompilado
pip install mysqlclient --only-binary=all

# Opción 3: Usar PyMySQL
pip uninstall mysqlclient
pip install pymysql
# Agregar a settings.py: import pymysql; pymysql.install_as_MySQLdb()
```

**❌ MySQL connection error**
```powershell
# Verificar que XAMPP MySQL esté iniciado
# Verificar .env: DB_HOST=127.0.0.1 (no localhost)
# Verificar puerto: DB_PORT=3306
```

**❌ Permission denied en venv\Scripts\activate**
```powershell
# Cambiar política de ejecución (como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# O usar Command Prompt en lugar de PowerShell
venv\Scripts\activate.bat
```

#### **Logs y Debugging**
```powershell
# Ver logs detallados de Django
python manage.py runserver --verbosity=2

# Verificar configuración
python manage.py check

# Ver configuración de BD
python manage.py dbshell --help
```

---

## 🧪 Endpoints Principales (propuesta inicial)

| Método | Endpoint                  | Descripción                                 |
| ------ | ------------------------- | ------------------------------------------- |
| `POST` | `/api/access/attempt/`    | Registrar intento de acceso (foto + código) |
| `GET`  | `/api/access/logs/`       | Obtener registros recientes                 |
| `GET`  | `/api/access/image/<id>/` | Ver imagen (solo admin)                     |
| `POST` | `/api/door/open/`         | Abrir puerta                                |
| `POST` | `/api/door/lock/`         | Activar o desactivar seguro                 |
| `GET`  | `/api/door/status/`       | Consultar estado actual                     |
| `POST` | `/api/users/create/`      | Crear usuario                               |
| `GET`  | `/api/users/list/`        | Listar usuarios                             |

---

## 👤 Autor

**Perseo de Jesús Osuna Padierna**  
Desarrollo de sistemas IoT y seguridad informática aplicada.

---

## 🧩 Licencia

Proyecto educativo con fines de desarrollo y demostración tecnológica.  
Licencia MIT (ajustable según implementación final).
