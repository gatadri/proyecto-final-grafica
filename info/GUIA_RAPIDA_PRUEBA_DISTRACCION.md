# 🚀 GUÍA RÁPIDA DE PRUEBA - Detección de Distracción Mejorada

## ⚡ Inicio Rápido (5 minutos)

### 1. Verificar Estado del Sistema

```bash
cd backend
python verificar_deteccion_distraccion.py
```

**Resultado esperado:**
- Lista de niños con historial
- Promedio de tiempo por niño
- Simulaciones de detección

---

### 2. Probar en la Interfaz

#### Paso 1: Iniciar servicios
```bash
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
ng serve
```

#### Paso 2: Completar ejercicios
1. Abre `http://localhost:4200`
2. Login como niño (usa el PIN de algún niño)
3. Abre consola del navegador (F12)
4. Entra a una tarea
5. Completa ejercicios

#### Paso 3: Ver logs
En la consola verás:
```
Análisis ML completo: {...}
Tiempo actual: 5000ms
Promedio histórico: 4000ms
Triple del promedio: 12000ms
✅ Normal (margen de 7000ms)
```

#### Paso 4: Forzar detección
- Tarda **intencionalmente** más de lo normal en un ejercicio
- Deberías ver:
```
🛑 PANTALLA DE DESCANSO ACTIVADA
📋 Razón: tiempo_excesivo
   Detalles: Tardó 15000ms (promedio: 4000ms)
```

---

### 3. Probar con API

```bash
# Reemplaza los IDs por los de tu base de datos
curl -X POST http://localhost:8000/api/tareas/ml/analizar-respuesta \
  -H "Content-Type: application/json" \
  -d '{
    "nino_id": 1,
    "ejercicio_id": 10,
    "tiempo_ms": 25000,
    "correcto": false,
    "tab_blur_count": 0,
    "idle_ms": 0,
    "erratic_clicks": 0
  }'
```

**Respuesta esperada:**
```json
{
  "distraccion": {
    "requiere_descanso": true,
    "motivo": "tiempo_excesivo",
    "detalles": "Tardó 25000ms (promedio: 4500ms)"
  },
  "tiempo_promedio_historico": 4500,
  "debug": {
    "tiempo_actual_ms": 25000,
    "triple_promedio_ms": 13500,
    "cantidad_datos_historicos": 30
  }
}
```

---

## 📊 Verificar en Base de Datos

### Ver historial de un niño
```sql
SELECT 
  id,
  time_spent_ms,
  correct,
  created_at
FROM tareas_progreso
WHERE student_id = 1
  AND time_spent_ms > 0
ORDER BY created_at DESC
LIMIT 30;
```

### Calcular promedio manualmente
```sql
SELECT 
  student_id,
  COUNT(*) as total_ejercicios,
  AVG(time_spent_ms) as promedio_ms,
  AVG(time_spent_ms) / 1000 as promedio_segundos,
  AVG(time_spent_ms) * 3 as umbral_3x_ms
FROM tareas_progreso
WHERE student_id = 1
  AND time_spent_ms > 0
  AND time_spent_ms < 180000
GROUP BY student_id;
```

---

## 🎯 Escenarios de Prueba

### Escenario 1: Niño con Historial Suficiente
```
✅ Niño con 30+ ejercicios completados
✅ Sistema usa promedio histórico
✅ Detección personalizada funcional
```

**Cómo probarlo:**
1. Elige un niño con historial
2. Completa ejercicio tardando 3x su promedio
3. Debe activarse pantalla de descanso

### Escenario 2: Niño Nuevo (< 5 ejercicios)
```
⚠️  Niño con menos de 5 ejercicios
✅ Sistema usa fallback (promedio sesión)
✅ Aún funcional pero menos preciso
```

**Cómo probarlo:**
1. Crea un niño nuevo
2. Completa 2-3 ejercicios rápido
3. Tarda mucho en el siguiente
4. Debe activarse por fallback

### Escenario 3: Errores Consecutivos
```
✅ Sistema detecta 3 errores seguidos
✅ Activa descanso independiente del tiempo
```

**Cómo probarlo:**
1. Comete 3 errores consecutivos
2. Debe activarse pantalla inmediatamente

---

## 🔍 Qué Buscar en los Logs

### ✅ Logs Correctos

```
Análisis ML completo: {
  distraccion: {
    requiere_descanso: false,
    focus_score: 0.8,
    motivo: null
  },
  tiempo_promedio_historico: 4500,
  debug: {
    tiempo_actual_ms: 5000,
    triple_promedio_ms: 13500,
    cantidad_datos_historicos: 30
  }
}
```

### ⚠️ Logs con Detección

```
═══════════════════════════════════
🛑 PANTALLA DE DESCANSO ACTIVADA
📋 Razón: tiempo_excesivo
   Detalles: Tardó 20000ms (promedio: 4500ms)
👤 Niño: Juan
📝 Ejercicio: 5/10
═══════════════════════════════════
```

### ❌ Error Común

```
Error: Niño no encontrado
```
**Solución:** Verifica que el nino_id existe

---

## 🐛 Troubleshooting Rápido

| Problema | Causa | Solución |
|----------|-------|----------|
| No aparece pantalla | Historial insuficiente | Completa más ejercicios |
| Logs no aparecen | Consola cerrada | Abre F12 en navegador |
| Error 500 API | Backend no corriendo | Inicia Django server |
| Sin promedio histórico | Tabla vacía | Completa ejercicios primero |

---

## 📝 Checklist de Verificación

Marca cuando completes cada paso:

- [ ] Backend corriendo sin errores
- [ ] Frontend corriendo en localhost:4200
- [ ] Base de datos MySQL conectada
- [ ] Script de verificación ejecutado
- [ ] Login como niño exitoso
- [ ] Consola del navegador abierta (F12)
- [ ] Ejercicios completados (al menos 5)
- [ ] Logs de ML visibles en consola
- [ ] Pantalla de descanso probada
- [ ] API endpoint testeado con curl/Postman

---

## 🎉 Resultado Esperado

Después de completar esta guía deberías:

✅ Ver el tiempo promedio histórico de cada niño
✅ Ver logs detallados en consola del navegador
✅ Ver la pantalla de descanso cuando se detecta distracción
✅ Entender cómo funciona el sistema personalizado
✅ Poder verificar en base de datos

---

## 📞 Ayuda Adicional

**Documentación completa:**
- `info/MEJORA_DETECCION_DISTRACCION_TIEMPO_PROMEDIO.md`
- `info/RESUMEN_MEJORA_DISTRACCION.txt`

**Scripts de ayuda:**
- `backend/verificar_deteccion_distraccion.py`

**Archivos modificados:**
- `backend/tareas/ml_utils.py`
- `backend/tareas/views.py`
- `frontend/src/app/modules/nino/tarea/nino-tarea.component.ts`

---

**¡Listo para probar! 🚀**
