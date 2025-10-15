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

- Python 3.11+
- Django 5.x
- Django Rest Framework
- MySQL 8.x
- ESP32 con cámara (por ejemplo, AI-Thinker o M5Camera)
- Conexión Wi-Fi estable
- Bootstrap 5 (frontend)
- OpenCV (opcional, para análisis facial)

---

## ⚙️ Instalación Básica

```bash
# Clonar repositorio
git clone https://github.com/usuario/smart-access-system.git
cd smart-access-system/backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
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
