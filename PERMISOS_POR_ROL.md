# 🔐 Control de Permisos por Rol

## Matriz de Permisos del Sistema

### 📋 Panel de Administración - Gestión de Usuarios

| Permiso | ADMIN | DIRECTOR | MAESTRO | ALUMNO |
|---------|-------|----------|---------|--------|
| Ver usuarios | ✅ | ✅ | ✅ | ❌ |
| Crear usuarios | ✅ | ✅ | ❌ | ❌ |
| Editar usuarios | ✅ | ✅ | ✅* | ❌ |
| Eliminar usuarios | ✅ | ❌ | ❌ | ❌ |
| Cambiar contraseña | ✅ | ✅ | ✅ | ❌ |
| Editar código de acceso | ✅ | ✅ | ❌ | ❌ |
| Modificar is_staff/is_superuser | ✅ | ✅ | ❌ | ❌ |

*MAESTRO puede editar datos básicos pero no permisos del sistema.

### 👤 Panel de Administración - Perfiles de Usuario

| Permiso | ADMIN | DIRECTOR | MAESTRO | ALUMNO |
|---------|-------|----------|---------|--------|
| Ver perfiles | ✅ | ✅ | ✅ | ❌ |
| Crear perfiles | ✅ | ✅ | ❌ | ❌ |
| Editar perfiles | ✅ | ✅ | ✅* | ❌ |
| Eliminar perfiles | ✅ | ❌ | ❌ | ❌ |
| Cambiar contraseña | ✅ | ✅ | ✅ | ❌ |
| Editar código de acceso | ✅ | ✅ | ❌ | ❌ |
| Cambiar rol | ✅ | ✅ | ✅ | ❌ |

*MAESTRO puede ver código de acceso pero no modificarlo.

### 🚪 Panel de Administración - Puertas

| Permiso | ADMIN | DIRECTOR | MAESTRO | ALUMNO |
|---------|-------|----------|---------|--------|
| Ver puertas | ✅ | ✅ | ✅ | ❌ |
| Crear puertas | ✅ | ✅ | ❌ | ❌ |
| Editar puertas | ✅ | ✅ | ❌ | ❌ |
| Eliminar puertas | ✅ | ❌ | ❌ | ❌ |
| Abrir/Cerrar puerta | ✅ | ✅ | ✅ | ❌ |
| Activar/Desactivar | ✅ | ✅ | ❌ | ❌ |

### 🔒 Panel de Administración - Seguros

| Permiso | ADMIN | DIRECTOR | MAESTRO | ALUMNO |
|---------|-------|----------|---------|--------|
| Ver seguros | ✅ | ✅ | ✅ | ❌ |
| Activar seguro | ✅ | ✅ | ✅ | ❌ |
| Desactivar seguro | ✅ | ✅ | ❌ | ❌ |

### 🔓 Sistema de Control de Acceso (Físico)

| Permiso | ADMIN | DIRECTOR | MAESTRO | ALUMNO |
|---------|-------|----------|---------|--------|
| Abrir puerta con código | ✅ | ✅ | ✅ | ✅ |
| Acceso si perfil inactivo | ❌ | ❌ | ❌ | ❌ |

---

## 🎯 Métodos del Modelo UserProfile

```python
# Todos los roles activos pueden abrir puertas físicamente
def puede_abrir_puerta(self):
    return self.activo

# Director, Maestro y Admin pueden gestionar usuarios
def puede_gestionar_usuarios(self):
    return self.rol in ['ADMIN', 'DIRECTOR', 'MAESTRO'] and self.activo

# Director, Maestro y Admin pueden controlar el seguro
def puede_controlar_seguro(self):
    return self.rol in ['ADMIN', 'DIRECTOR', 'MAESTRO'] and self.activo

# Solo Director y Admin pueden desactivar seguro principal
def puede_desactivar_seguro(self):
    return self.rol in ['ADMIN', 'DIRECTOR'] and self.activo
```

---

## 📝 Resumen de Roles

### 👨‍💼 ADMIN (Administrador)
- **Acceso completo** a todas las funciones del sistema
- Puede eliminar usuarios, perfiles y puertas
- Control total sobre permisos y configuración
- Puede editar código de acceso de cualquier usuario
- Puede cambiar contraseña de cualquier usuario

### 🏫 DIRECTOR
- Gestión completa de usuarios (crear, editar, cambiar contraseña)
- Control total de puertas y seguros
- Puede editar códigos de acceso
- **No puede eliminar** usuarios ni puertas
- **No puede modificar** permisos de sistema (is_staff, is_superuser)

### 👨‍🏫 MAESTRO
- Puede **ver y editar** datos básicos de usuarios
- Puede **cambiar contraseñas** de usuarios
- Puede **ver** código de acceso pero **no modificarlo**
- Puede activar seguros pero no desactivarlos
- **No puede crear ni eliminar** usuarios
- **No puede modificar** permisos de sistema

### 🎓 ALUMNO
- **Solo acceso físico** con código de acceso
- **Sin acceso** al panel de administración
- No puede gestionar nada en el sistema
- Solo puede abrir puertas con su código personal

---

## 🔑 Cambio de Contraseña

En el panel de administración, ahora aparece un enlace **"🔑 Cambiar contraseña"** en:

1. **Lista de Usuarios**: Columna "Contraseña" con enlace directo
2. **Lista de Perfiles de Usuarios**: Columna "Contraseña" con enlace directo
3. **Detalle de Usuario**: Botón de cambio de contraseña en la parte superior

**Permisos requeridos**: ADMIN, DIRECTOR o MAESTRO

---

## ⚙️ Implementación Técnica

### Control de Permisos en Admin

```python
# En UserAdmin y UserProfileAdmin

def has_view_permission(self, request, obj=None):
    # ADMIN, DIRECTOR, MAESTRO pueden ver

def has_change_permission(self, request, obj=None):
    # ADMIN, DIRECTOR, MAESTRO pueden editar

def has_add_permission(self, request):
    # Solo ADMIN y DIRECTOR pueden crear

def has_delete_permission(self, request, obj=None):
    # Solo ADMIN puede eliminar
```

### Campos de Solo Lectura por Rol

```python
def get_readonly_fields(self, request, obj=None):
    # MAESTRO: no puede editar is_staff, is_superuser, groups, permissions
    # MAESTRO: no puede editar codigo_acceso en UserProfile
    # DIRECTOR y ADMIN: acceso completo
```
