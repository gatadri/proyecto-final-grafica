# 🔧 SOLUCIÓN: Datos no se muestran en interfaz

## Problema
Los datos SÍ existen en MySQL pero NO se muestran en la interfaz del director.

## ✅ Corrección Aplicada

He corregido el componente `director-dashboard.component.ts` para:
1. Cargar ambas APIs en paralelo usando `forkJoin`
2. Inicializar `stats` con valores por defecto
3. Agregar logs de consola para debugging

## 🚀 Para Aplicar la Corrección

### Paso 1: Reiniciar el Frontend
```bash
# Detener el servidor Angular (Ctrl+C)
# Reiniciar:
cd frontend
ng serve
```

### Paso 2: Limpiar Caché del Navegador
1. Abrir DevTools (F12)
2. Click derecho en botón de recargar
3. Seleccionar "Vaciar caché y recargar de manera forzada"

O usar: **Ctrl + Shift + R** (Windows/Linux) o **Cmd + Shift + R** (Mac)

### Paso 3: Verificar en Consola del Navegador
1. Abrir DevTools (F12)
2. Ir a pestaña "Console"
3. Hacer login como director
4. Ir al dashboard
5. Deberías ver estos logs:
   ```
   Estadísticas: {total_estudiantes: X, ...}
   Usuarios: [{id: 1, nombre: "...", role: "..."}, ...]
   Profesores contados: X
   Padres contados: X
   Stats finales: {total_profesores: X, total_padres: X, ...}
   ```

## 🔍 Si Aún No Se Muestra

### Verificar que el endpoint devuelve datos
```bash
# En terminal:
cd backend
python manage.py shell
```

```python
from users.models import User

# Ver todos los usuarios
usuarios = User.objects.all()
for u in usuarios:
    print(f"{u.role}: {u.nombre} {u.apellido}")

# Contar por rol
print(f"Directores: {User.objects.filter(role='director').count()}")
print(f"Profesores: {User.objects.filter(role='profesor').count()}")
print(f"Padres: {User.objects.filter(role='padre').count()}")
```

### Verificar endpoint directamente
```bash
# Obtener token
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"director@correo.com","password":"password"}'

# Usar el token recibido:
curl http://localhost:8000/api/usuarios \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

Debería retornar un array JSON con usuarios.

## 🐛 Debugging en el Navegador

### Si no aparecen los logs:
1. El componente no se está cargando
2. Verificar rutas en `app-routing-module.ts`

### Si los logs muestran arrays vacíos:
1. El endpoint no está devolviendo datos
2. Verificar que el backend está corriendo
3. Verificar que hay datos en MySQL

### Si los logs muestran error 401:
1. El token expiró
2. Cerrar sesión y volver a hacer login

### Si los logs muestran error 403:
1. El usuario no tiene permisos
2. Verificar que el usuario es director

## 📊 Qué Ver en la Consola

### Éxito (debe verse así):
```javascript
Estadísticas: {
  total_estudiantes: 10,
  total_tareas_completadas: 45,
  total_xp_sistema: 4500,
  total_monedas_sistema: 1500,
  ...
}

Usuarios: [
  {id: 1, nombre: "Director", apellido: "Admin", role: "director", ...},
  {id: 2, nombre: "Prof", apellido: "Uno", role: "profesor", ...},
  {id: 3, nombre: "Padre", apellido: "Uno", role: "padre", hijos: [...]},
  ...
]

Profesores contados: 2
Padres contados: 5

Stats finales: {
  total_profesores: 2,
  total_padres: 5,
  total_ninos: 10,
  ...
}
```

### Problema (arrays vacíos):
```javascript
Estadísticas: {...}
Usuarios: []  ← PROBLEMA
Profesores contados: 0
Padres contados: 0
```

## ✅ Verificación Final

Después de reiniciar el frontend:
1. Login: http://localhost:4200/login
2. Email: director@correo.com
3. Password: password
4. Ver dashboard: http://localhost:4200/director/dashboard
5. **Debe mostrar:**
   - Total Profesores: > 0
   - Total Padres: > 0
   - Total Estudiantes: > 0

## 📝 Cambios Realizados en el Código

### Antes:
```typescript
loadDashboard(): void {
  this.api.get('director/estadisticas-generales').subscribe(data => {
    this.stats = { ... };
    this.loadUsuariosCount(); // Se ejecuta DESPUÉS
    this.loading = false;
  });
}

loadUsuariosCount(): void {
  this.api.get('usuarios').subscribe(users => {
    this.stats.total_profesores = ...;
    this.stats.total_padres = ...;
  });
}
```

**Problema:** `loading = false` se ejecuta ANTES de que se carguen los usuarios.

### Después:
```typescript
loadDashboard(): void {
  forkJoin({
    estadisticas: this.api.get('director/estadisticas-generales'),
    usuarios: this.api.get('usuarios')
  }).subscribe(({ estadisticas, usuarios }) => {
    // Ambas llamadas completas ANTES de procesar
    const profesores = usuarios.filter(u => u.role === 'profesor').length;
    const padres = usuarios.filter(u => u.role === 'padre').length;
    
    this.stats = {
      total_profesores: profesores,
      total_padres: padres,
      ...
    };
    
    this.loading = false; // Ahora SÍ tiene todos los datos
  });
}
```

**Solución:** Ambas llamadas se hacen en paralelo y solo se muestra cuando ambas terminan.

## 🎯 Resumen

1. ✅ Corregido timing de carga de datos
2. ✅ Agregados logs para debugging
3. ✅ Inicialización correcta de variables
4. 🔄 **Debes reiniciar el servidor Angular**
5. 🔄 **Debes limpiar caché del navegador**

---

**Si después de esto aún no funciona, revisa los logs de la consola del navegador y comparte el error específico que aparece.**
