# Cómo Probar el Sistema de Reportes por Tema

## ✅ Sistema ya configurado y listo

Todo está funcionando. Solo necesitas probarlo.

## 🎯 Prueba Rápida (5 minutos)

### Opción 1: Ver Reporte con Datos Existentes (Más Rápido)

Si Alejandra u otro niño ya completó tareas:

1. **Abrir navegador:**
   ```
   http://localhost:4200/reporte-detallado/17
   ```
   (17 es el ID de Alejandra, puedes usar 18 para Carla, 19 para Mariano)

2. **Si no muestra datos**, continuar con Opción 2

### Opción 2: Generar Datos de Prueba

1. **Entrar como niño:**
   - URL: `http://localhost:4200/nino`
   - Usuario: Alejandra
   - PIN: 8778

2. **Ir a "Mis Tareas"**

3. **Completar una tarea de multiplicación** (ej: Tarea ID 11)
   - **IMPORTANTE:** Falla intencionalmente en ejercicios de tabla del 11
   - Ejemplo: Si aparece "11 × 8 = ?", selecciona respuesta incorrecta
   - Falla al menos 3-4 ejercicios de tabla del 11

4. **Completar la tarea** (no importa si fallas todos)

5. **Ver reporte:**
   ```
   http://localhost:4200/reporte-detallado/17
   ```

6. **Deberías ver:**
   ```
   Análisis Detallado por Área
   
   📊 Multiplicación
   ┌──────────────┬─────────┬──────────┬──────────┐
   │ Tema         │ Errores │ Aciertos │ % Error  │
   ├──────────────┼─────────┼──────────┼──────────┤
   │ Tabla 11     │    4    │    1     │  80.0%   │
   │ Tabla 12     │    2    │    3     │  40.0%   │
   └──────────────┴─────────┴──────────┴──────────┘
   
   Recomendaciones:
   - Reforzar multiplicación: especialmente Tabla 11.
   ```

## 🔧 Probar API Directamente

### 1. Verificar que ejercicios están etiquetados
```bash
cd backend
python etiquetar_ejercicios.py
```

Deberías ver:
```
Total actualizado: 66 ejercicios
Resumen por tema:
   multiplicacion - tabla_12: 7 ejercicios
   multiplicacion - tabla_11: 4 ejercicios
   ...
```

### 2. Probar endpoint de reporte
```bash
curl "http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id=17"
```

O en el navegador:
```
http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id=17
```

Deberías ver JSON con estructura:
```json
{
  "nino": {...},
  "reporte_por_subtema": [...],
  "resumen": {...}
}
```

## 📧 Probar Notificación por Email

```bash
curl -X POST "http://localhost:8000/api/tareas/ml/notificar" \
  -H "Content-Type: application/json" \
  -d '{"nino_id": 17}'
```

Respuesta esperada:
```json
{
  "message": "Notificaciones preparadas",
  "data": {
    "nino": {...},
    "padre": {"email": "...", "nombre": "..."},
    "profesor": {"email": "...", "nombre": "..."},
    "errores_detectados": [...]
  }
}
```

## 🗄️ Verificar Base de Datos

Abrir phpMyAdmin o HeidiSQL:

### Ver ejercicios etiquetados:
```sql
SELECT id, pregunta, tema, subtema 
FROM tareas_ejercicio 
WHERE tema LIKE 'tabla%' 
LIMIT 10;
```

Resultado esperado:
```
+----+------------------+-----------+----------------+
| id | pregunta         | tema      | subtema        |
+----+------------------+-----------+----------------+
| 16 | Cuanto es 4×11?  | tabla_11  | multiplicacion |
| 18 | 11 × 5 = ?       | tabla_11  | multiplicacion |
| 23 | 12 × 7 = ?       | tabla_12  | multiplicacion |
+----+------------------+-----------+----------------+
```

### Ver análisis de errores:
```sql
SELECT * FROM tareas_analisiserrortema WHERE nino_id = 17;
```

Si no hay datos, es porque el niño no ha completado tareas aún.

## 🚨 Troubleshooting

### Problema: "No hay datos disponibles"

**Causa:** El niño no ha completado ninguna tarea aún.

**Solución:** 
1. Entrar como niño
2. Completar al menos una tarea
3. Volver a ver reporte

### Problema: "Ejercicios sin tema"

**Causa:** Script de etiquetado no se ejecutó.

**Solución:**
```bash
cd backend
python etiquetar_ejercicios.py
```

### Problema: "Migration error"

**Causa:** Migración no aplicada.

**Solución:**
```bash
cd backend
python manage.py migrate
```

### Problema: "Endpoint 404"

**Causa:** Backend no está corriendo.

**Solución:**
```bash
cd backend
python manage.py runserver
```

### Problema: "CORS error en frontend"

**Causa:** Frontend no puede conectar con backend.

**Solución:** Verificar que en `settings.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

## 📱 Agregar Botón en Dashboard de Profesor

Para acceder fácilmente a los reportes desde el dashboard del profesor:

**profesor-dashboard.component.html:**
```html
<!-- En la lista de estudiantes -->
<div *ngFor="let estudiante of estudiantes">
  <h5>{{ estudiante.nombre }} {{ estudiante.apellido }}</h5>
  
  <!-- NUEVO BOTÓN -->
  <a [routerLink]="['/reporte-detallado', estudiante.id]" 
     class="btn btn-info btn-sm">
    <i class="fas fa-chart-bar me-2"></i>
    Ver Reporte de Errores
  </a>
</div>
```

**app.routes.ts:**
```typescript
import { ReporteDetalladoComponent } from './components/reporte-detallado.component';

export const routes: Routes = [
  // ... rutas existentes
  {
    path: 'reporte-detallado/:ninoId',
    component: ReporteDetalladoComponent
  }
];
```

## ✅ Checklist de Verificación

- [ ] Backend corriendo en `localhost:8000`
- [ ] Frontend corriendo en `localhost:4200`
- [ ] Migración 0012 aplicada (`python manage.py migrate`)
- [ ] Ejercicios etiquetados (66 ejercicios con tema)
- [ ] Endpoint responde: `http://localhost:8000/api/tareas/ml/reporte-detallado?nino_id=17`
- [ ] Al menos un niño completó una tarea
- [ ] Componente accesible: `http://localhost:4200/reporte-detallado/17`

## 🎓 Datos de Prueba

### Niños disponibles:
- **Alejandra** - ID: 17, PIN: 8778
- **Carla** - ID: 18, PIN: 5079
- **Mariano** - ID: 19, PIN: 1220

### Tareas ML disponibles:
- **Tarea 11** - Multiplicación (4 ejercicios tabla del 11)
- **Tarea 12** - División (ejercicios variados)
- **Tarea 13** - Fracciones
- **Tarea 14** - Mixta

### Ejercicios con tabla del 11:
```sql
SELECT id, pregunta FROM tareas_ejercicio WHERE tema = 'tabla_11';
```

## 🎉 ¡Listo para Probar!

Todo está configurado y funcionando. Solo necesitas:
1. Completar una tarea como niño (fallando algunos ejercicios)
2. Ver el reporte generado
3. ¡Disfrutar del sistema de análisis por tema!

---

**¿Tienes dudas?** Revisa:
- `SISTEMA_REPORTES_DETALLADOS.md` - Documentación completa
- `IMPLEMENTACION_COMPLETA_REPORTES.md` - Resumen de implementación
