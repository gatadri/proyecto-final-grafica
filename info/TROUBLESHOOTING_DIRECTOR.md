# TROUBLESHOOTING - MÓDULO DIRECTOR

## 🔍 PROBLEMAS COMUNES Y SOLUCIONES

---

## ❌ Error: "Usuario director no existe"

### Síntomas
- No se puede hacer login
- Error 400 en `/api/login`

### Solución
```bash
cd backend
python verificar_director.py
```
Este script creará o corregirá el usuario director automáticamente.

**Credenciales:**
- Email: `director@correo.com`
- Password: `password`

---

## ❌ Error: "No se muestran usuarios"

### Síntomas
- La página de usuarios aparece vacía
- Console del navegador muestra error 401 o 403

### Solución 1: Verificar autenticación
1. Cerrar sesión
2. Volver a hacer login
3. Verificar que el token se guarda correctamente

### Solución 2: Verificar que hay usuarios en la BD
```bash
cd backend
python verificar_sistema_director.py
```

Si no hay usuarios, ejecutar un script de seed:
```bash
python seed.py
```

---

## ❌ Dashboard muestra todos los valores en 0

### Síntomas
- Dashboard carga pero todos los números son 0
- No hay errores en consola

### Causa
No hay datos en la base de datos

### Solución
```bash
cd backend
# Crear datos de prueba
python llenar_datos_prueba.py
# O ejecutar seed completo
python seed.py
```

---

## ❌ Logs aparece vacío

### Síntomas
- La página de logs carga pero no muestra eventos
- No hay errores

### Causa
No hay actividad registrada en el sistema

### Solución
1. Hacer que algún estudiante complete una tarea
2. Crear una tarea nueva como profesor
3. Ejecutar script para generar actividad:
```bash
cd backend
python llenar_datos_prueba.py
```

---

## ❌ Error 500 en `/api/director/estadisticas-generales`

### Síntomas
- Dashboard no carga
- Error 500 en la petición

### Posibles causas y soluciones

#### Causa 1: Migración faltante
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

#### Causa 2: Error en la consulta
Ver logs del servidor Django y verificar el error específico:
```bash
# En la terminal donde corre el servidor
# Buscar el traceback completo
```

---

## ❌ CORS Error en el frontend

### Síntomas
- Error en consola del navegador: "CORS policy blocked"
- Las peticiones no llegan al backend

### Solución
Verificar configuración CORS en `backend/backend_django/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

CORS_ALLOW_CREDENTIALS = True
```

Si no existe `django-cors-headers`:
```bash
cd backend
pip install django-cors-headers
```

Agregar a INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]
```

Agregar a MIDDLEWARE:
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

---

## ❌ Token inválido o expirado

### Síntomas
- Error 401 "Unauthorized"
- Funciona inicialmente pero deja de funcionar después

### Solución
1. Cerrar sesión
2. Volver a hacer login
3. Si persiste, limpiar localStorage:
```javascript
// En consola del navegador
localStorage.clear();
```

---

## ❌ Números no coinciden entre Dashboard y Reportes

### Síntomas
- Dashboard muestra X estudiantes
- Reportes muestra Y estudiantes (diferente)

### Causa
Este problema YA ESTÁ SOLUCIONADO en las correcciones.

### Verificación
Si persiste, verificar que:
1. Usaste los archivos actualizados
2. Reiniciaste el servidor backend
3. Limpiaste caché del navegador (Ctrl+Shift+R)

---

## 🔧 COMANDOS ÚTILES

### Reiniciar todo desde cero
```bash
# Backend
cd backend
python manage.py flush --no-input
python manage.py migrate
python seed.py
python verificar_director.py

# Frontend
cd frontend
rm -rf node_modules/.cache
ng serve --port 4200
```

### Ver logs en tiempo real
```bash
# Backend Django
cd backend
python manage.py runserver

# Frontend Angular (en otra terminal)
cd frontend
ng serve
```

### Verificar estado del sistema
```bash
cd backend
python verificar_sistema_director.py
```

### Probar endpoints manualmente
```bash
cd backend
python probar_endpoints_director.py
```

---

## 🐛 DEBUGGING AVANZADO

### Habilitar modo debug en Django
En `backend/backend_django/settings.py`:
```python
DEBUG = True
```

### Ver queries SQL en Django
```python
# En views.py, temporalmente
from django.db import connection
print(connection.queries)
```

### Ver peticiones en Angular
Abrir DevTools del navegador:
1. F12 o Ctrl+Shift+I
2. Network tab
3. Filtrar por "XHR"
4. Ver request/response de cada petición

---

## 📞 CHECKLIST DE VERIFICACIÓN

Antes de reportar un problema, verifica:

- [ ] El servidor Django está corriendo (`python manage.py runserver`)
- [ ] El servidor Angular está corriendo (`ng serve`)
- [ ] El usuario director existe (`python verificar_director.py`)
- [ ] Hay datos en la base de datos (`python verificar_sistema_director.py`)
- [ ] El token JWT es válido (hacer login nuevamente)
- [ ] No hay errores en la consola del navegador (F12)
- [ ] No hay errores en la terminal del servidor Django
- [ ] Los archivos actualizados están en su lugar
- [ ] Se reiniciaron ambos servidores después de los cambios

---

## 🆘 ÚLTIMO RECURSO

Si nada funciona:

### Opción 1: Reset completo
```bash
# Backup de la base de datos si es necesario
cd backend
cp db.sqlite3 db.sqlite3.backup

# Reset
python manage.py flush --no-input
python manage.py migrate
python seed.py
python verificar_director.py
```

### Opción 2: Revisar versiones
```bash
# Python
python --version  # Debe ser 3.8+

# Django
cd backend
pip show django

# Node
node --version  # Debe ser 16+

# Angular
cd frontend
ng version
```

---

## 📝 LOGS IMPORTANTES

### Django
- Ubicación: Terminal donde corre `manage.py runserver`
- Ver errores detallados con traceback completo

### Angular
- Ubicación: Consola del navegador (F12 > Console)
- Ver errores de TypeScript y peticiones HTTP

### Base de datos
```bash
cd backend
python manage.py dbshell
# Luego:
.tables  # Ver todas las tablas
SELECT * FROM users_user;  # Ver usuarios
SELECT * FROM tareas_nino;  # Ver estudiantes
```

---

Para problemas no cubiertos aquí, revisar:
- CORRECCIONES_DIRECTOR.md - Documentación completa
- GUIA_RAPIDA_DIRECTOR.md - Guía rápida de uso
