# ✓ CHECKLIST DE VERIFICACIÓN - MÓDULO DIRECTOR

Usa este checklist para verificar que todas las correcciones funcionan correctamente.

---

## 🔧 PREPARACIÓN

### Backend
- [ ] Servidor Django corriendo: `cd backend && python manage.py runserver`
- [ ] Usuario director existe: `python verificar_director.py`
- [ ] Base de datos tiene datos: `python verificar_sistema_director.py`

### Frontend
- [ ] Servidor Angular corriendo: `cd frontend && ng serve`
- [ ] Puerto 4200 disponible: http://localhost:4200
- [ ] No hay errores de compilación

---

## 🧪 TESTS BÁSICOS

### 1. Login del Director
- [ ] Ir a: http://localhost:4200/login
- [ ] Email: `director@correo.com`
- [ ] Password: `password`
- [ ] Login exitoso
- [ ] Redirige a dashboard del director

**Si falla:** Ejecutar `python verificar_director.py`

---

## 📊 DASHBOARD

URL: http://localhost:4200/director/dashboard

### Verificar Números
- [ ] Total Profesores > 0
- [ ] Total Padres > 0
- [ ] Total Estudiantes > 0
- [ ] Total Tareas > 0

### Verificar Estadísticas
- [ ] Tareas Completadas muestra número real
- [ ] XP Total del Sistema muestra número real
- [ ] Monedas en Circulación muestra número real
- [ ] Logros Obtenidos muestra número real

### Verificar Botones
- [ ] Botón "Gestionar Usuarios" funciona
- [ ] Botón "Inventario Tienda" funciona
- [ ] Botón "Ver Reportes" funciona
- [ ] Botón "Ver Estadísticas" funciona
- [ ] Botón "Log de Actividades" funciona

**Si números son 0:** Ejecutar `python llenar_datos_prueba.py`

---

## 👥 GESTIÓN DE USUARIOS

URL: http://localhost:4200/director/usuarios

### Verificar Lista
- [ ] Se muestra lista de usuarios
- [ ] Cada usuario tiene: nombre, email, rol, estado
- [ ] Se ven usuarios de tipo: director, profesor, padre

### Verificar Acciones
- [ ] Botón "Crear Usuario" abre formulario
- [ ] Puede crear un nuevo profesor
- [ ] Puede crear un nuevo padre con hijos
- [ ] Puede suspender un usuario
- [ ] Puede activar un usuario suspendido
- [ ] Puede ver detalles de hijos (padres)
- [ ] Puede eliminar un usuario

### Formulario de Creación
- [ ] Campos: nombre, apellido, email, password, rol
- [ ] Si rol es "padre", aparece sección de hijos
- [ ] Puede agregar múltiples hijos
- [ ] Cada hijo tiene: nombre, apellido, PIN, profesor
- [ ] Validaciones funcionan correctamente

**Si no aparecen usuarios:** Verificar token JWT y hacer login nuevamente

---

## 📝 LOGS DE ACTIVIDAD

URL: http://localhost:4200/director/logs

### Verificar Datos
- [ ] Se muestran eventos del sistema
- [ ] Eventos ordenados por fecha (más recientes primero)
- [ ] Cada evento tiene: fecha, usuario, descripción, tipo

### Verificar Tipos de Eventos
- [ ] Aparecen eventos de tipo "tarea" (badge verde)
- [ ] Aparecen eventos de tipo "practica" (badge azul)
- [ ] Aparecen eventos de tipo "logro" (badge amarillo)
- [ ] Aparecen eventos de tipo "sistema" (badge gris)

### Verificar Contenido
- [ ] Eventos de tareas: "Completó tarea [nombre] (X pts)"
- [ ] Eventos de logros: "Obtuvo logro [nombre]"
- [ ] Eventos de prácticas: "Completó práctica libre (X pts)"
- [ ] Eventos de sistema: "Creó la tarea [nombre]"

**Si está vacío:**
1. Hacer que un estudiante complete una tarea
2. O ejecutar `python llenar_datos_prueba.py`

---

## 📈 REPORTES

URL: http://localhost:4200/director/reportes

### Verificar Estadísticas
- [ ] Total Estudiantes coincide con dashboard
- [ ] Tareas Completadas coincide con dashboard
- [ ] Promedio de Rendimiento calculado correctamente
- [ ] Monedas del Sistema coincide con dashboard
- [ ] XP Total coincide con dashboard

### Verificar Gráficas/Tablas
- [ ] Rendimiento Semanal muestra datos
- [ ] Tareas por Tipo muestra distribución
- [ ] Distribución de Niveles muestra datos

### Verificar Exportación
- [ ] Botón "Descargar PDF" visible
- [ ] Al hacer click, genera PDF
- [ ] PDF contiene toda la información
- [ ] Nombre del archivo: `reporte-general-YYYY-MM-DD.pdf`

---

## 🎯 CONSISTENCIA DE DATOS

### Comparar Números

#### Dashboard vs Reportes
- [ ] Total Estudiantes: Dashboard ______ = Reportes ______
- [ ] Tareas Completadas: Dashboard ______ = Reportes ______
- [ ] Monedas: Dashboard ______ = Reportes ______
- [ ] XP: Dashboard ______ = Reportes ______

**IMPORTANTE:** Los números DEBEN ser idénticos en ambas vistas.

#### Script de Verificación
Ejecutar y comparar:
```bash
cd backend
python verificar_sistema_director.py
```

Números del script:
- Total Estudiantes: ______
- Tareas Completadas: ______
- Monedas Sistema: ______
- XP Sistema: ______

**Deben coincidir con Dashboard y Reportes**

---

## 🔍 VERIFICACIÓN DE ENDPOINTS

### Prueba Manual con curl

#### 1. Obtener Token
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"director@correo.com","password":"password"}'
```
- [ ] Retorna token
- [ ] Retorna datos del usuario

#### 2. Obtener Usuarios
```bash
curl http://localhost:8000/api/usuarios \
  -H "Authorization: Bearer {TOKEN}"
```
- [ ] Retorna array de usuarios
- [ ] Incluye información de hijos (padres)

#### 3. Obtener Estadísticas
```bash
curl http://localhost:8000/api/director/estadisticas-generales \
  -H "Authorization: Bearer {TOKEN}"
```
- [ ] Retorna objeto con estadísticas
- [ ] Incluye total_estudiantes, tareas_completadas, etc.

#### 4. Obtener Logs
```bash
curl http://localhost:8000/api/director/logs \
  -H "Authorization: Bearer {TOKEN}"
```
- [ ] Retorna array de logs
- [ ] Ordenados por fecha descendente

### O usar script automático
```bash
cd backend
python probar_endpoints_director.py
```
- [ ] Todos los tests pasan
- [ ] No hay errores

---

## 🐛 VERIFICACIÓN DE ERRORES

### Consola del Navegador (F12)
- [ ] No hay errores en rojo
- [ ] No hay warnings críticos
- [ ] Peticiones HTTP retornan 200 OK

### Terminal Django
- [ ] No hay errores 500
- [ ] No hay warnings críticos
- [ ] Todas las queries ejecutan correctamente

### Terminal Angular
- [ ] Compilación exitosa
- [ ] No hay errores de TypeScript
- [ ] No hay warnings críticos

---

## ⚡ TESTS DE PERFORMANCE

### Tiempos de Carga
- [ ] Dashboard carga en < 2 segundos
- [ ] Usuarios carga en < 2 segundos
- [ ] Logs carga en < 2 segundos
- [ ] Reportes carga en < 3 segundos

### Navegación
- [ ] Cambiar entre secciones es fluido
- [ ] No hay lag al hacer scroll
- [ ] Botones responden inmediatamente

---

## 🎨 VERIFICACIÓN VISUAL

### Dashboard
- [ ] Cards con colores correctos (azul, verde, naranja, celeste)
- [ ] Iconos visibles
- [ ] Layout responsive
- [ ] Texto legible

### Usuarios
- [ ] Tabla formateada correctamente
- [ ] Badges de rol con colores (azul, verde, naranja)
- [ ] Badges de estado (verde activo, rojo suspendido)
- [ ] Botones alineados

### Logs
- [ ] Tabla ordenada
- [ ] Badges de tipo con colores correctos
- [ ] Fechas formateadas
- [ ] Scroll funciona si hay muchos logs

### Reportes
- [ ] Gráficas/tablas visibles
- [ ] Colores consistentes
- [ ] PDF generado con formato correcto

---

## ✅ RESULTADO FINAL

### Resumen de Tests
- Dashboard: ___/13 tests pasados
- Usuarios: ___/11 tests pasados
- Logs: ___/10 tests pasados
- Reportes: ___/9 tests pasados
- Consistencia: ___/4 tests pasados
- Endpoints: ___/4 tests pasados
- Errores: ___/3 checks pasados
- Performance: ___/4 checks pasados
- Visual: ___/4 checks pasados

### Total: ___/62 tests

**META: 62/62 ✅**

---

## 🚨 SI ALGO FALLA

1. Revisar [TROUBLESHOOTING_DIRECTOR.md](./TROUBLESHOOTING_DIRECTOR.md)
2. Ejecutar scripts de verificación
3. Revisar logs de ambos servidores
4. Limpiar caché del navegador
5. Reiniciar servidores

---

## 📋 CHECKLIST RÁPIDO

Para verificación rápida, MÍNIMO verificar:

- [ ] ✅ Login funciona
- [ ] ✅ Dashboard muestra números reales
- [ ] ✅ Usuarios lista correctamente
- [ ] ✅ Logs muestra eventos reales
- [ ] ✅ Reportes coincide con dashboard
- [ ] ✅ No hay errores en consola
- [ ] ✅ Todos los endpoints responden

**Si estos 7 pasan, el sistema está OK ✓**

---

<div align="center">

## 🎉 ¡FELICITACIONES!

Si todos los tests pasan, el módulo del director está completamente funcional.

**Fecha de verificación:** __________________  
**Verificado por:** __________________  
**Estado:** ☐ Aprobado  ☐ Con observaciones

</div>
